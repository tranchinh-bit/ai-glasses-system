from __future__ import annotations

import asyncio
from typing import Any, Dict

import aiohttp

from ...utils.logging_util import setup_logger
from ...utils.config_loader import ConfigLoader


class NavClient:
    """Client gọi REST để lấy hướng dẫn điều hướng từ backend/mobile."""

    def __init__(self, config_loader: ConfigLoader):
        self._cfg = config_loader.load("network")["backend"]
        self._logger = setup_logger("NavClient")

    async def get_next_instruction(self, location: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self._cfg['base_url']}/api/v1/nav/next"
        timeout = aiohttp.ClientTimeout(total=self._cfg["timeout_sec"])
        async with aiohttp.ClientSession(timeout=timeout) as sess:
            try:
                async with sess.post(url, json=location) as resp:
                    resp.raise_for_status()
                    return await resp.json()
            except Exception as e:
                self._logger.warning("Nav request failed: %s", e)
                return {}
