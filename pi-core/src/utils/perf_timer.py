import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def perf_timer() -> Iterator[float]:
    start = time.perf_counter()
    yield lambda: time.perf_counter() - start  # type: ignore[misc]
