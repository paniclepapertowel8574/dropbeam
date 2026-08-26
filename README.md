# ⚡ DropBeam

[English](README.md) | [فارسی](README.fa.md)

[![CI](https://github.com/FarhanDEV2010/dropbeam/actions/workflows/ci.yml/badge.svg)](https://github.com/FarhanDEV2010/dropbeam/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141%2B-009688)
![License](https://img.shields.io/badge/license-MIT-green)

**Beam files and text between your devices over the local network.** Like AirDrop, but in your browser — no cables, no cloud, no accounts, no app installs.

## 🪄 How it works

1. Run DropBeam on your computer → it shows a **QR code**
2. Scan it with your phone (or open the URL on any device on the same Wi-Fi)
3. Devices **discover each other automatically** and appear live
4. Tap a device → drag & drop files, or beam text
5. The other side gets it **instantly** — files even auto-copy received text to clipboard

Works with your internet completely cut off. Files never leave your network.

## ✨ Highlights

- 🔍 **Zero-config peer discovery** — every open tab joins the room via WebSocket, live
- 📁 Drag & drop with real upload progress (streamed to disk, up to 512 MB per file)
- 💬 Text beaming with automatic clipboard copy on the receiving device
- 📱 QR join — phone connects in two taps, nothing to install
- 🕵️ Privacy-first: one-time download links, files auto-purged after 60 minutes, nothing persisted
- 🏷️ Fun device names — meet `SwiftOtter` and `CosmicFalcon` instead of IP addresses
- ✅ 21 integration tests: registration, presence, delivery flows, expiry purge, one-time links
- 🔄 CI: tests on Python 3.11–3.13 + live server smoke test + Docker build

## 🚀 Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://localhost:8000**, scan the QR with your phone, and beam something.

With Docker:

```bash
docker compose up --build
```

> Both devices must be on the same local network (same Wi-Fi / hotspot).

## 📖 API Overview

| Method | Endpoint                      | Description                          |
| ------ | ----------------------------- | ------------------------------------ |
| POST   | `/api/register`               | Register this device, get an ID      |
| GET    | `/qr.svg`                     | QR code of this server's address     |
| WS     | `/ws?id=...`                  | Live presence + delivery events      |
| POST   | `/api/send/{id}/text`         | Beam text to a device                |
| POST   | `/api/send/{id}/file`         | Beam file(s) to a device             |
| GET    | `/download/{token}`           | One-time download link               |
| GET    | `/health`                     | Health check                         |

## 🧪 Running Tests

```bash
pytest -v
```

## 🏗️ Architecture Notes

- **No database.** Pure in-memory registry — state is meant to die with the process.
- **WebSocket presence protocol**: join/leave events fan out personalized peer lists; the dashboard reconnects automatically.
- **Streamed uploads**: incoming files are written to disk in 1 MB chunks with size enforcement mid-stream.
- **One-time tokens**: each download link self-destructs after first use; a background sweeper purges expired files.

## 📄 License

MIT — see [LICENSE](LICENSE).
