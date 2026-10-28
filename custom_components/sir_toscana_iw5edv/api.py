"""HTTP client for SIR Toscana."""

from __future__ import annotations

import asyncio
import dataclasses
import html
import json
import logging
import re
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientError, ClientSession

from .const import (
    REQUEST_TIMEOUT,
    STATION_LIST_URL,
    STATIONS_URL,
    STATION_TYPES,
    STATION_URL,
)

_LOGGER = logging.getLogger(__name__)

_ARRAY_RE = re.compile(
    r'new\s+Array\(\s*"(?P<id>TOS\d+)"\s*,\s*"(?P<field1>(?:\\.|[^"])*)"'
    r'(?:\s*,\s*"(?P<field2>(?:\\.|[^"])*)")?',
    re.IGNORECASE,
)
_STATION_ID_RE = re.compile(r"TOS\d+", re.IGNORECASE)
_TRANSPORT_SUFFIX_RE = re.compile(r"\s+\((?:RADIO|GPRS)\)\s*$", re.IGNORECASE)


class SirToscanaApiError(Exception):
    """Base exception for SIR Toscana API errors."""


class SirToscanaConnectionError(SirToscanaApiError):
    """Raised when SIR Toscana cannot be reached."""


class SirToscanaInvalidResponseError(SirToscanaApiError):
    """Raised when SIR Toscana returns an invalid response."""


class SirToscanaStationNotFoundError(SirToscanaApiError):
    """Raised when a requested station cannot be found."""


class SirToscanaAmbiguousStationError(SirToscanaApiError):
    """Raised when a station name matches more than one station."""


@dataclass(frozen=True, slots=True)
class SirStation:
    """A SIR Toscana station."""

    station_id: str
    name: str
    municipality: str = ""
    province: str = ""


def _clean_text(value: Any) -> str:
    """Unescape HTML entities and collapse whitespace."""
    if not isinstance(value, str):
        return ""
    return " ".join(html.unescape(value).split())


def parse_station_list(
    text: str,
    station_type: str | None = None,
) -> list[SirStation]:
    """Extract station identifiers and names from a SIR monitoring page."""
    stations: list[SirStation] = []

    for match in _ARRAY_RE.finditer(text):
        # Hydrometric rows are structured as:
        # ID, river, station, province, ...
        # The other supported monitoring tables put the station name
        # immediately after the ID.
        raw_name = (
            match.group("field2")
            if station_type == "idro" and match.group("field2")
            else match.group("field1")
        )

        name = raw_name.replace(r'\"', '"').replace(r"\\", "\\")
        stations.append(
            SirStation(
                station_id=match.group("id"),
                name=_clean_text(name),
            )
        )

    return stations


def parse_station_geojson(text: str) -> list[SirStation]:
    """Extract stations from the SIR station list JSON endpoint."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as err:
        raise SirToscanaInvalidResponseError from err

    features = data.get("features") if isinstance(data, dict) else None
    if not isinstance(features, list):
        raise SirToscanaInvalidResponseError

    stations: list[SirStation] = []

    for feature in features:
        if not isinstance(feature, dict):
            continue

        station_id = _clean_text(feature.get("IDStazione")).upper()
        name = _clean_text(feature.get("Nome"))
        if not _STATION_ID_RE.fullmatch(station_id) or not name:
            continue

        stations.append(
            SirStation(
                station_id=station_id,
                name=name,
                municipality=_clean_text(feature.get("Comune")),
                province=_clean_text(feature.get("Provincia")).upper(),
            )
        )

    return stations


def canonical_station_name(value: str) -> str:
    """Normalize a station name for matching across SIR monitoring tables."""
    normalized = " ".join(html.unescape(value).casefold().strip().split())
    normalized = _TRANSPORT_SUFFIX_RE.sub("", normalized)
    return normalized.strip()


def _merge_stations(current: SirStation | None, new: SirStation) -> SirStation:
    """Combine two records of the same station, keeping the best details."""
    if current is None:
        return new

    return dataclasses.replace(
        current,
        # The shortest published name is the one without RADIO/GPRS suffixes.
        name=new.name if len(new.name) < len(current.name) else current.name,
        municipality=current.municipality or new.municipality,
        province=current.province or new.province,
    )


class SirToscanaApi:
    """Async client for the public SIR Toscana monitoring endpoints."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def async_get_station_data(self, station_id: str) -> dict[str, Any]:
        """Return the complete JSON payload for one station."""
        text = await self._async_get_text(STATION_URL.format(station_id=station_id))

        try:
            data = json.loads(text)
        except json.JSONDecodeError as err:
            raise SirToscanaInvalidResponseError from err

        if not isinstance(data, dict) or not data:
            raise SirToscanaInvalidResponseError

        return data

    async def async_get_stations(self) -> list[SirStation]:
        """Discover station names and IDs from the public SIR station lists."""
        stations: dict[str, SirStation] = {}

        # The complete list and the per-type lists differ slightly, so both
        # are combined. An empty type returns every station.
        sources = ("", *STATION_TYPES)
        results = await asyncio.gather(
            *(self._async_get_stations_for_type(source) for source in sources),
            return_exceptions=True,
        )

        for source, result in zip(sources, results, strict=True):
            if isinstance(result, BaseException):
                _LOGGER.warning(
                    "Unable to load the SIR station list for type '%s': %r",
                    source or "all",
                    result,
                )
                continue

            for station in result:
                stations[station.station_id] = _merge_stations(
                    stations.get(station.station_id), station
                )

        if not stations:
            raise SirToscanaConnectionError

        _LOGGER.debug("Loaded %d SIR stations", len(stations))

        return sorted(
            stations.values(),
            key=lambda station: (
                station.name.casefold(),
                station.municipality.casefold(),
                station.station_id,
            ),
        )

    async def async_find_station(self, station_name: str) -> SirStation:
        """Find one station by its published name, case-insensitively."""
        requested = canonical_station_name(station_name)
        if not requested:
            raise SirToscanaStationNotFoundError

        stations = await self.async_get_stations()

        exact = [
            station
            for station in stations
            if canonical_station_name(station.name) == requested
        ]
        if len(exact) == 1:
            return exact[0]
        if len(exact) > 1:
            raise SirToscanaAmbiguousStationError

        partial = [
            station
            for station in stations
            if requested in canonical_station_name(station.name)
        ]
        if len(partial) == 1:
            return partial[0]
        if len(partial) > 1:
            raise SirToscanaAmbiguousStationError

        raise SirToscanaStationNotFoundError

    async def _async_get_stations_for_type(
        self,
        station_type: str,
    ) -> list[SirStation]:
        """Read one SIR station list, falling back to the monitoring table."""
        try:
            text = await self._async_get_text(
                STATION_LIST_URL.format(station_type=station_type)
            )
            stations = parse_station_geojson(text)
            if not stations:
                raise SirToscanaInvalidResponseError
        except SirToscanaApiError as err:
            if not station_type:
                raise

            _LOGGER.warning(
                "SIR station list for type '%s' unavailable (%r), "
                "falling back to the monitoring table",
                station_type,
                err,
            )
        else:
            return stations

        text = await self._async_get_text(
            STATIONS_URL.format(station_type=station_type)
        )
        return parse_station_list(text, station_type)

    async def _async_get_text(self, url: str) -> str:
        """Return the body of a SIR page."""
        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                response = await self._session.get(url)
                response.raise_for_status()
                return await response.text()
        except (TimeoutError, ClientError) as err:
            raise SirToscanaConnectionError(f"{url}: {err!r}") from err
        except UnicodeDecodeError as err:
            raise SirToscanaInvalidResponseError(url) from err
