import subprocess
from pathlib import Path
from typing import Optional

from ...utils.logging_util import setup_logger
from ...utils.config_loader import ConfigLoader


class TtsPlayer:
    """
    Player TTS đơn giản:
      - hiện tại giả định đã có 1 lệnh CLI `say_vi` (offline) hoặc dùng `espeak`.
      - sau có thể thay bằng Edge-TTS, Piper...
    """

    def __init__(self, config_loader: ConfigLoader):
        self._cfg = config_loader.load("audio")
        self._logger = setup_logger("TtsPlayer")

    def speak(self, text: str, profile: Optional[str] = None) -> None:
        if not text:
            return
        try:
            # Tối thiểu: dùng espeak (nhẹ, có sẵn trên Pi)
            subprocess.Popen(["espeak", "-v", "vi+f3", text])
        except Exception as e:
            self._logger.warning("Failed to play TTS: %s", e)
