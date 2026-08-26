import secrets
import tempfile
import time
from pathlib import Path
from typing import Any

from .config import settings

ADJECTIVES = [
    "Swift", "Brave", "Cosmic", "Neon", "Silent", "Rapid", "Lucky", "Wild",
    "Golden", "Electric", "Turbo", "Shadow", "Crystal", "Hyper", "Mega",
]
ANIMALS = [
    "Otter", "Falcon", "Tiger", "Panda", "Dolphin", "Fox", "Wolf", "Eagle",
    "Cobra", "Panther", "Koala", "Raven", "Lynx", "Orca", "Heron",
]

STORAGE = Path(tempfile.gettempdir()) / "dropbeam"
clients: dict[str, dict[str, Any]] = {}
sockets: dict[str, Any] = {}
transfers: dict[str, dict[str, Any]] = {}

STORAGE.mkdir(parents=True, exist_ok=True)


def _browser(ua: str) -> str:
    ua = ua.lower()
    for name, marker in [
        ("Edge", "edg/"), ("Chrome", "chrome"), ("Firefox", "firefox"),
        ("Safari", "safari"), ("Opera", "opera"),
    ]:
        if marker in ua:
            return name
    return "Browser"


def create_client(user_agent: str) -> dict:
    client_id = secrets.token_urlsafe(8)
    kind = "Phone" if any(
        k in user_agent.lower() for k in ("mobile", "android", "iphone")
    ) else "Desktop"
    name = f"{secrets.choice(ADJECTIVES)}{secrets.choice(ANIMALS)}"
    client = {"id": client_id, "name": f"{name} ({kind})", "kind": kind}
    clients[client_id] = client
    return client


def get_client(client_id: str) -> dict | None:
    return clients.get(client_id)


def connect(client_id: str, websocket: Any):
    sockets[client_id] = websocket


def disconnect(client_id: str):
    sockets.pop(client_id, None)


def connected_ids() -> list[str]:
    return list(sockets.keys())


def list_peers(exclude_id: str | None = None) -> list[dict]:
    return [
        {"id": c["id"], "name": c["name"], "kind": c["kind"]}
        for cid, c in clients.items()
        if cid in sockets and cid != exclude_id
    ]


def add_transfer(path: Path, filename: str) -> str:
    token = secrets.token_urlsafe(16)
    transfers[token] = {
        "path": str(path),
        "filename": filename,
        "created_at": time.monotonic(),
    }
    return token


def pop_transfer(token: str) -> dict | None:
    return transfers.pop(token, None)


def cleanup_expired():
    ttl = settings.file_ttl_minutes * 60
    now = time.monotonic()
    expired = [t for t, v in transfers.items() if now - v["created_at"] > ttl]
    for token in expired:
        entry = transfers.pop(token)
        try:
            Path(entry["path"]).unlink(missing_ok=True)
        except OSError:
            pass
