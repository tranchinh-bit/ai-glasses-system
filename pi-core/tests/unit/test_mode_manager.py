from src.core.mode_manager import ModeManager


def test_mode_manager_auto_fallback():
    system_cfg = {
        "offload_mode": "AUTO",
        "network": {"phone_heartbeat_timeout_sec": 5},
    }
    power_profiles = {"profiles": {}}
    mm = ModeManager(system_cfg, power_profiles)

    # ban đầu chưa thấy phone -> LOCAL
    assert mm.decide_mode() == "LOCAL"

    mm.notify_phone_alive()
    assert mm.decide_mode() == "PHONE"
