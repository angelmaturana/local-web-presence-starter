"""Minimal FastAPI web server with Render keep-alive support."""

import os
import threading
import time
import urllib.request
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Posicionamiento Web Valdemoro", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


def build_url(request: Request, path: str) -> str:
    """Build a public URL using the forwarded scheme and host."""
    scheme = "https" if request.headers.get("x-forwarded-proto") == "https" else "http"
    host = request.headers.get("host", "localhost:8000")
    return f"{scheme}://{host}{path}"


def keep_alive_ping() -> None:
    """Ping the public service periodically when deployed on Render."""
    time.sleep(30)

    external_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not external_url:
        print("[Keep-Alive] RENDER_EXTERNAL_URL not set - skipping keep-alive (local mode)")
        return

    ping_url = f"{external_url.rstrip('/')}/keepalive"
    interval = int(os.environ.get("KEEPALIVE_INTERVAL", "270"))
    print(f"[Keep-Alive] Engine started - pinging {ping_url} every {interval}s")

    while True:
        try:
            request = urllib.request.Request(ping_url, method="GET")
            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status == 200:
                    print(f"[Keep-Alive] Pinged {ping_url} -> {response.status}")
        except Exception as exc:
            print(f"[Keep-Alive] Ping failed: {exc}")

        time.sleep(interval)


threading.Thread(target=keep_alive_ping, daemon=True).start()


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return a simple health status for monitoring services."""
    return {
        "status": "healthy",
        "message": "Web server is running",
    }


@app.get("/")
async def home_page(request: Request):
    """Render the site's main page."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"canonical_url": build_url(request, "/")},
    )


@app.get("/keepalive")
async def keepalive() -> PlainTextResponse:
    """Endpoint used by the internal keep-alive request and monitors."""
    return PlainTextResponse("OK", status_code=200)


if __name__ == "__main__":
    import uvicorn

    print("Starting web server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
