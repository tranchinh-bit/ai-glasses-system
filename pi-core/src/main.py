import asyncio
from loguru import logger

from src.utils.config_loader import load_system_config, load_power_profiles
from src.core.orchestrator import Orchestrator


def main():
    logger.add("data/logs/core.log", rotation="1 MB", retention=5)
    logger.info("AI Glasses Pi-Core starting...")

    system_cfg = load_system_config()
    power_profiles = load_power_profiles()

    orch = Orchestrator(system_cfg, power_profiles)

    try:
        asyncio.run(orch.run())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt, shutting down...")
    except Exception as e:
        logger.exception(f"Fatal error in orchestrator: {e}")


if __name__ == "__main__":
    main()
