from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Dict, List, Optional
from loguru import logger

from .. import models

router = APIRouter()

# ---- Connection Manager ----


class WSManager:
    """
    Quản lý kết nối WebSocket cho Family App.
    - Mỗi device_id có thể có nhiều client (nhiều người thân).
    - Nếu device_id = "all" thì client nhận event của mọi thiết bị.
    """

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.global_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, device_id: Optional[str]):
        await websocket.accept()
        if device_id and device_id != "all":
            self.active_connections.setdefault(device_id, []).append(websocket)
            logger.info(f"WS connected for device={device_id}, total={len(self.active_connections[device_id])}")
        else:
            self.global_connections.append(websocket)
            logger.info(f"WS connected for ALL devices, total={len(self.global_connections)}")

    def disconnect(self, websocket: WebSocket, device_id: Optional[str]):
        if device_id and device_id != "all":
            conns = self.active_connections.get(device_id, [])
            if websocket in conns:
                conns.remove(websocket)
        else:
            if websocket in self.global_connections:
                self.global_connections.remove(websocket)

    async def _send_json_safe(self, websocket: WebSocket, data: dict):
        try:
            await websocket.send_json(data)
        except Exception as e:
            logger.warning(f"Error sending WS message: {e}")

    def _broadcast(self, payload: dict, device_id: str):
        # Gửi tới device cụ thể
        for ws in list(self.active_connections.get(device_id, [])):
            import asyncio
            asyncio.create_task(self._send_json_safe(ws, payload))

        # Gửi tới những connection listen ALL
        for ws in list(self.global_connections):
            import asyncio
            asyncio.create_task(self._send_json_safe(ws, payload))

    def broadcast_alert(self, alert: models.Alert):
        payload = {
            "type": "alert",
            "payload": {
                "id": alert.id,
                "device_id": alert.device_id,
                "level": alert.level,
                "type": alert.type,
                "message": alert.message,
                "rule_id": alert.rule_id,
                "created_at": alert.created_at.isoformat(),
                "handled": alert.handled,
            },
        }
        self._broadcast(payload, alert.device_id)

    def broadcast_location(self, loc: models.Location):
        payload = {
            "type": "location",
            "payload": {
                "id": loc.id,
                "device_id": loc.device_id,
                "lat": loc.lat,
                "lon": loc.lon,
                "accuracy_m": loc.accuracy_m,
                "created_at": loc.created_at.isoformat(),
            },
        }
        self._broadcast(payload, loc.device_id)


ws_manager = WSManager()


# ---- WebSocket endpoint ----


@router.websocket("/ws/family")
async def family_ws(websocket: WebSocket, device_id: Optional[str] = Query(default="all")):
    """
    Family app connect:
    ws://host/ws/family?device_id=glasses-001
    hoặc
    ws://host/ws/family?device_id=all
    """
    await ws_manager.connect(websocket, device_id)
    try:
        while True:
            # hiện tại server chỉ push, nhưng vẫn nhận message nếu client gửi ping...
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, device_id)
        logger.info(f"WS disconnected for device={device_id}")
