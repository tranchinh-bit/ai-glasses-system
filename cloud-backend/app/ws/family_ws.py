from __future__ import annotations

import json
from typing import Set

from fastapi import WebSocket, WebSocketDisconnect

from ..models import Alert

_connections: Set[WebSocket] = set()


async def family_ws_endpoint(ws: WebSocket):
    """WebSocket cho Family App – chỉ nhận alert, không cần gửi dữ liệu lên."""
    await ws.accept()
    _connections.add(ws)
    try:
        while True:
            # Family app có thể gửi ping, nhưng hiện tại ta bỏ qua nội dung.
            await ws.receive_text()
    except WebSocketDisconnect:
        _connections.discard(ws)
    except Exception:
        _connections.discard(ws)


async def broadcast_alert(alert: Alert) -> None:
    """Gửi alert tới tất cả Family App đang kết nối."""
    if not _connections:
        return

    data = {
        "id": alert.id,
        "device_id": alert.device_id,
        "hazard_code": alert.hazard_code,
        "severity": alert.severity,
        "title": alert.title,
        "message": alert.message,
        "created_at": alert.created_at.isoformat() if alert.created_at else None,
    }
    msg = json.dumps({"type": "alert", "data": data})

    to_remove: Set[WebSocket] = set()
    for ws in _connections:
        try:
            await ws.send_text(msg)
        except Exception:
            to_remove.add(ws)

    for ws in to_remove:
        _connections.discard(ws)
