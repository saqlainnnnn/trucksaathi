from __future__ import annotations

from fastapi import FastAPI

from api.websocket import router

app = FastAPI(
    title="TruckSaathi Dashboard",
)

app.include_router(router)


@app.get("/")
def health():
    return {
        "status": "ok",
    }