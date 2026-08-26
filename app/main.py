from contextlib import asynccontextmanager, suppress

import asyncio
import io

import qrcode
import qrcode.image.svg
from fastapi import (
    FastAPI,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import registry
from .config import settings
from .registry import STORAGE


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = None
    if settings.scheduler_enabled:
        task = asyncio.create_task(_cleanup_loop())
    yield
    if task:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


async def _cleanup_loop():
    while True:
        await asyncio.sleep(300)
        registry.cleanup_expired()


app = FastAPI(
    title="DropBeam API",
    description="Beam files and text between your devices over the local network. No cables, no cloud, no accounts.",
    version="1.0.0",
    lifespan=lifespan,
)


class TextPayload(BaseModel):
    sender_id: str
    text: str = Field(min_length=1, max_length=10_000)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


@app.post("/api/register", tags=["session"])
def register(request: Request):
    return registry.create_client(request.headers.get("user-agent", ""))


@app.get("/qr.svg", tags=["session"])
def qr_code(request: Request):
    url = str(request.base_url).rstrip("/")
    img = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage, box_size=14)
    buf = io.BytesIO()
    img.save(buf)
    return Response(buf.getvalue(), media_type="image/svg+xml")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, id: str):
    client = registry.get_client(id)
    if not client:
        await websocket.close(code=4004)
        return
    await websocket.accept()
    registry.connect(id, websocket)
    await broadcast_peers()
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        registry.disconnect(id)
        await broadcast_peers()


async def broadcast_peers():
    for cid in registry.connected_ids():
        try:
            await registry.sockets[cid].send_json(
                {"event": "peers", "peers": registry.list_peers(exclude_id=cid)}
            )
        except Exception:
            registry.disconnect(cid)


async def _require_socket(target_id: str) -> WebSocket:
    sock = registry.sockets.get(target_id)
    if not sock:
        raise HTTPException(status_code=404, detail="target device is offline")
    return sock


@app.post("/api/send/{target_id}/text", tags=["transfer"])
async def send_text(target_id: str, payload: TextPayload):
    sender = registry.get_client(payload.sender_id)
    if not sender or target_id == payload.sender_id:
        raise HTTPException(status_code=400, detail="invalid sender")
    sock = await _require_socket(target_id)
    await sock.send_json(
        {
            "event": "text",
            "from": sender["name"],
            "text": payload.text,
        }
    )
    return {"delivered": True}


@app.post("/api/send/{target_id}/file", tags=["transfer"])
async def send_file(
    target_id: str,
    sender_id: str = Form(...),
    files: list[UploadFile] = File(...),
):
    sender = registry.get_client(sender_id)
    if not sender or target_id == sender_id:
        raise HTTPException(status_code=400, detail="invalid sender")
    sock = await _require_socket(target_id)

    max_bytes = settings.max_file_mb * 1024 * 1024
    delivered = []
    for upload in files:
        dest = STORAGE / f"{upload.filename}"
        size = 0
        with dest.open("wb") as out:
            while chunk := await upload.read(1024 * 1024):
                size += len(chunk)
                if size > max_bytes:
                    out.close()
                    dest.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=413,
                        detail=f"file too large (max {settings.max_file_mb} MB)",
                    )
                out.write(chunk)
        token = registry.add_transfer(dest, upload.filename or "file")
        delivered.append({"token": token, "name": upload.filename, "size": size})

    await sock.send_json({"event": "files", "from": sender["name"], "files": delivered})
    return {"delivered": True}


@app.get("/download/{token}", include_in_schema=False)
def download(token: str):
    entry = registry.pop_transfer(token)
    if not entry:
        raise HTTPException(status_code=404, detail="transfer expired or already downloaded")
    path = STORAGE / entry["filename"]
    return FileResponse(entry["path"], filename=entry["filename"])


@app.get("/", include_in_schema=False)
def home():
    return FileResponse("app/static/index.html")


app.mount("/static", StaticFiles(directory="app/static"), name="static")
