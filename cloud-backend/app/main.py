from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import engine, Base
from .routers import locations, alerts, health
from .ws.family_ws import family_ws_endpoint

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    # Tạo bảng nếu chưa có
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# REST routers
app.include_router(locations.router)
app.include_router(alerts.router)
app.include_router(health.router)


# WebSocket cho Family App
@app.websocket(settings.ws_family_path)
async def family_ws(ws: WebSocket):
    await family_ws_endpoint(ws)
