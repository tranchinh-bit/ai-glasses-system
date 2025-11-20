from __future__ import annotations

import asyncio
import json
from typing import Any

import aiohttp

from ...utils.logging_util import setup_logger
from ...utils.config_loader import ConfigLoader
from ...utils.event_bus import EventBus
from ...core.events import HazardEvent


class WsClient:
    def __init__(self, bus: EventBus, config_loader: ConfigLoader) -> None:
        self._bus = bus
        self._cfg = config_loader.load("network")["io_hub"]
        self._system_cfg = config_loader.load("system")
        self._logger = setup_logger("WsClient")
        self._session: aiohttp.ClientSession | None = None
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._reconnect_task: asyncio.Task | None = None

    async def init(self) -> None:
        self._session = aiohttp.ClientSession()
        asyncio.create_task(self._connect_loop())

    async def _connect_loop(self) -> None:
        url = self._cfg["ws_url"]
        interval = self._cfg["reconnect_interval_sec"]
        max_interval = self._cfg["max_reconnect_interval_sec"]

        while True:
            try:
                self._logger.info("Connecting to WS %s", url)
                assert self._session is not None
                async with self._session.ws_connect(url) as ws:
                    self._ws = ws
                    self._logger.info("WS connected")
                    interval = self._cfg["reconnect_interval_sec"]
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            await self._handle_message(msg.data)
                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            break
            except Exception as e:
                self._logger.warning("WS error: %s", e)

            self._ws = None
            self._logger.info("WS disconnected, retry in %s sec", interval)
            await asyncio.sleep(interval)
            interval = min(interval * 2, max_interval)

    async def _handle_message(self, data: str) -> None:
        # Tạm thời chỉ log; sau có thể xử lý lệnh từ mobile
        self._logger.debug("WS recv: %s", data)

    async def send_hazard(self, event: HazardEvent) -> None:
        if not self._ws:
            return
        payload: dict[str, Any] = {
            "device_id": self._system_cfg["device_id"],
            "hazard_code": event.hazard_code,
            "severity": event.severity,
            "message": event.message,
            "related_objects": event.related_objects,
        }
        try:
            await self._ws.send_str(json.dumps({"type": "hazard", "data": payload}))
        except Exception as e:
            self._logger.warning("Failed to send hazard: %s", e)
