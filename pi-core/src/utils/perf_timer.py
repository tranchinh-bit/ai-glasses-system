import time
from contextlib import contextmanager
from typing import Iterator
from loguru import logger


@contextmanager
def perf_timer(label: str) -> Iterator[None]:
    start = time.time()
    try:
        yield
    finally:
        dur = (time.time() - start) * 1000.0
        logger.debug(f"[PERF] {label}: {dur:.1f} ms")
