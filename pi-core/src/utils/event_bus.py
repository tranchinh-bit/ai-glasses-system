import asyncio
from typing import Any, Callable, Dict, List, Coroutine


class EventBus:
    """Event bus đơn giản dựa trên asyncio."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Any], Coroutine[Any, Any, None]]]] = {}

    def subscribe(self, event_type: str, handler: Callable[[Any], Coroutine[Any, Any, None]]) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    async def publish(self, event_type: str, payload: Any) -> None:
        handlers = self._subscribers.get(event_type, [])
        for h in handlers:
            # fire-and-forget nhưng không block
            asyncio.create_task(h(payload))
