import asyncio
from pathlib import Path

from .core.orchestrator import Orchestrator


async def async_main() -> None:
    root = Path(__file__).resolve().parents[1]
    orch = Orchestrator(root)
    await orch.init()
    await orch.run()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
