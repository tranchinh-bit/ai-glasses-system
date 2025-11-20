import wave
from pathlib import Path
from typing import Optional

import pyaudio  # nếu sau này muốn thu âm; hiện tại có thể comment nếu chưa cài


class Recorder:
    def __init__(self, output_dir: Path, rate: int = 16000, channels: int = 1):
        self.output_dir = output_dir
        self.rate = rate
        self.channels = channels
        self.format = pyaudio.paInt16  # type: ignore[attr-defined]
        self.chunk = 1024
        self._pa: Optional[pyaudio.PyAudio] = None  # type: ignore[name-defined]

    def record_to_file(self, filename: str, seconds: int) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path = self.output_dir / filename

        self._pa = pyaudio.PyAudio()  # type: ignore[name-defined]
        stream = self._pa.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk,
        )

        frames = []
        for _ in range(0, int(self.rate / self.chunk * seconds)):
            data = stream.read(self.chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        self._pa.terminate()

        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self._pa.get_sample_size(self.format))  # type: ignore[union-attr]
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(frames))

        return path
