class TTSPlayer:
    """
    Stub – có thể triển khai bằng local TTS (espeak, Coqui) hoặc gửi qua phone.
    """

    def __init__(self, audio_cfg):
        self.audio_cfg = audio_cfg

    def speak(self, text: str):
        # TODO: call local TTS hoặc gửi WS tới phone
        print(f"[TTS] {text}")
