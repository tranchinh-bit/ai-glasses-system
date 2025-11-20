import asyncio
from collections import defaultdict
from typing import Any, Awaitable, Callable, Dict, List

EventHandler = Callable[[str, Any], Awaitable[None]]


class EventBus:
    """Event bus async nhẹ cho nội bộ Pi-core."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[EventHandler]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def subscribe(self, event_type: str, handler: EventHandler) -> None:
        async with self._lock:
            self._subscribers[event_type].append(handler)

    async def publish(self, event_type: str, payload: Any) -> None:
        handlers: List[EventHandler]
        async with self._lock:
            handlers = list(self._subscribers.get(event_type, []))

        for h in handlers:
            # fire and forget
            asyncio.create_task(h(event_type, payload))
