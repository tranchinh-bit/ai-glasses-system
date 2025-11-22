import asyncio
import time
import json
from typing import Any, Dict

import websockets
from loguru import logger

from src.utils.event_bus import EventBus


class WSClient:
    """
    WebSocket client từ Pi -> User App trên điện thoại.
    - Gửi health, danger, vision frame (nếu offload PHONE).
    - Nhận detection result, config update, v.v.

    Ở đây implement skeleton kết nối, heartbeat, phone_alive.
    """

    def __init__(
        self,
        ws_url: str,
        event_bus: EventBus,
        mode_manager,
        security_cfg: Dict[str, Any],
        device_id: str,
    ):
        self.ws_url = ws_url
        self.event_bus = event_bus
        self.mode_manager = mode_manager
        self.device_id = device_id
        self.shared_secret = security_cfg.get("auth", {}).get("shared_secret", "")
        self._running = True

    async def run(self) -> None:
        backoff = 1
        while self._running:
            try:
                logger.info(f"[WS] Connecting to phone at {self.ws_url}...")
                async with websockets.connect(self.ws_url, ping_interval=10) as ws:
                    logger.info("[WS] Connected to phone.")
                    backoff = 1
                    await self._handshake(ws)
                    await self._recv_loop(ws)
            except Exception as e:
                logger.warning(f"[WS] Connection error: {e}")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 30)

    async def _handshake(self, ws):
        msg = {
            "type": "hello",
            "device_id": self.device_id,
            "ts": int(time.time() * 1000),
        }
        await ws.send(json.dumps(msg))

    async def _recv_loop(self, ws):
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except Exception:
                logger.warning(f"[WS] Invalid JSON from phone: {raw!r}")
                continue

            mtype = msg.get("type")
            if mtype == "heartbeat":
                await self.event_bus.publish("phone_alive", None)
            elif mtype == "config_update":
                # TODO: parse and apply (change base_mode, profile...)
                logger.info(f"[WS] Config update from phone: {msg}")
            elif mtype == "detection_result":
                # TODO: forward to fusion / danger analyzer
                pass
            else:
                logger.debug(f"[WS] Unknown message type: {mtype}")
