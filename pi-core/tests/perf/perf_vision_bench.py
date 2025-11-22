import time

from src.services.power_manager.power_manager import PowerManager
from src.utils.event_bus import EventBus


def main():
    system_cfg = {"default_power_profile": "BALANCED"}
    power_profiles = {
        "profiles": {"BALANCED": {"max_camera_fps": 10}}
    }
    pm = PowerManager(system_cfg, power_profiles, EventBus())

    start = time.time()
    frames = 100
    for _ in range(frames):
        # TODO: gọi vision_local với frame fake
        pass
    dur = time.time() - start
    print(f"{frames} frames in {dur:.2f}s => {frames/dur:.2f} FPS")


if __name__ == "__main__":
    main()
