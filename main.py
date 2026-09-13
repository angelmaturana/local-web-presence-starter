"""SEO Valdemoro website application."""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote
from xml.sax.saxutils import escape

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


def _safe_int(value: str, fallback: int) -> int:
    try:
        return int(value)
    except ValueError:
        return fallback


@dataclass(frozen=True)
class Settings:
    """Runtime settings that may be overridden by Render environment variables."""

    site_url: str = os.getenv("SITE_URL", "http://localhost:8000").rstrip("/")
    site_name: str = os.getenv("SITE_NAME", "SEO Valdemoro")
    phone: str = "615 09 68 57"
    phone_e164: str = "+34615096857"
    whatsapp_message: str = "Hola SEO Valdemoro, quiero mejorar la presencia digital de mi negocio."
    render_external_url: str | None = os.getenv("RENDER_EXTERNAL_URL")
    keepalive_interval: int = max(60, _safe_int(os.getenv("KEEPALIVE_INTERVAL", "270"), 270))

    @property
    def whatsapp_url(self) -> str:
        return f"https://wa.me/{self.phone_e164.removeprefix('+')}?text={quote(self.whatsapp_message)}"


settings = Settings()
templates = Jinja2Templates(directory=TEMPLATES_DIR)

SERVICES: dict[str, dict[str, Any]] = {
    "desarrollo-web-valdemoro": {
        "title": "Desarrollo web móvil en Valdemoro",
        "short_title": "Web móvil",
        "eyebrow": "01 / Web que trabaja",
        "intro": "Una web rápida, clara y pensada para convertir visitas desde el móvil en conversaciones reales.",
        "description": "Diseñamos sitios web mobile-first para comercios y pequeñas empresas de Valdemoro, con una arquitectura sencilla, contenidos útiles y llamadas a la acción visibles.",
        "points": [
            "Arquitectura mobile-first y navegación sin fricción.",
            "Páginas preparadas para crecer con nuevos servicios.",
            "Contenido orientado a llamadas, mapas y conversaciones.",
        ],
    },
    "seo-local-google-maps-valdemoro": {
        "title": "SEO local y Google Maps en Valdemoro",
        "short_title": "SEO local",
        "eyebrow": "02 / Ser encontrable",
        "intro": "Ordenamos las señales locales que ayudan a que tu negocio aparezca cuando alguien ya está buscando lo que ofreces.",
        "description": "Trabajamos la presencia local con información consistente, páginas de servicio útiles, perfiles de mapas y una estrategia de opiniones basada en experiencias reales.",
        "points": [
            "Consistencia de nombre, dirección, teléfono y web.",
            "Páginas y contenidos vinculados a Valdemoro y su entorno.",
            "Mejora de la información que recibe quien te encuentra.",
        ],
    },
    "posicionamiento-ia-chatgpt-valdemoro": {
        "title": "Posicionamiento en IA para negocios de Valdemoro",
        "short_title": "SEO + IA",
        "eyebrow": "03 / Responder mejor",
        "intro": "Convertimos el conocimiento de tu negocio en contenido claro, verificable y fácil de interpretar por buscadores y asistentes de IA.",
        "description": "La visibilidad en respuestas generativas empieza por una entidad bien descrita: servicios concretos, datos coherentes, experiencia demostrable y respuestas directas a preguntas reales.",
        "points": [
            "Contenido con hechos, contexto y lenguaje natural.",
            "Preguntas frecuentes para búsquedas conversacionales.",
            "Señales de autoridad conectadas con fuentes públicas.",
        ],
    },
    "pack-digital-valdemoro": {
        "title": "Pack digital integral para PyMEs de Valdemoro",
        "short_title": "Pack integral",
        "eyebrow": "04 / Todo conectado",
        "intro": "Una base digital completa para dejar de improvisar entre la web, los mapas y el contenido.",
        "description": "Combinamos estrategia, desarrollo web y posicionamiento local en un plan comprensible, con prioridades visibles y entregables que tu equipo pueda mantener.",
        "points": [
            "Diagnóstico inicial y mapa de prioridades.",
            "Web, SEO local y contenidos en una misma dirección.",
            "Acompañamiento cercano, sin lenguaje de agencia opaco.",
        ],
    },
}

NAV_ITEMS = (
    ("Inicio", "/"),
    ("Servicios", "/#servicios"),
    ("Casos", "/casos-exito-valdemoro"),
    ("Nosotros", "/sobre-nosotros"),
    ("Blog", "/blog"),
)
PUBLIC_PATHS = (
    "/",
    "/casos-exito-valdemoro",
    "/sobre-nosotros",
    "/blog",
    *[f"/servicios/{slug}" for slug in SERVICES],
)


def page_context(request: Request, title: str, description: str, **values: object) -> dict[str, object]:
    """Return the shared template context for a public page."""
    return {
        "request": request,
        "site_name": settings.site_name,
        "site_url": settings.site_url,
        "canonical_url": f"{settings.site_url}{request.url.path}",
        "page_title": title,
        "page_description": description,
        "nav_items": NAV_ITEMS,
        "services": SERVICES,
        "contact_phone": settings.phone,
        "contact_phone_e164": settings.phone_e164,
        "whatsapp_url": settings.whatsapp_url,
        **values,
    }


async def keep_alive_loop() -> None:
    """Ping the public Render service until application shutdown."""
    if not settings.render_external_url:
        return

    ping_url = f"{settings.render_external_url.rstrip('/')}/keepalive"
    import urllib.request

    await asyncio.sleep(30)
    while True:
        try:
            def ping() -> int:
                request = urllib.request.Request(ping_url, method="GET")
                with urllib.request.urlopen(request, timeout=10) as response:
                    return response.status

            status = await asyncio.to_thread(ping)
            if status != 200:
                print(f"[Keep-Alive] Unexpected response: {status}")
        except Exception as exc:
            print(f"[Keep-Alive] Ping failed: {exc}")
        await asyncio.sleep(settings.keepalive_interval)


@asynccontextmanager
async def lifespan(_: FastAPI):
    keepalive_task = None
    if settings.render_external_url:
        keepalive_task = asyncio.create_task(keep_alive_loop())
    yield
    if keepalive_task:
        keepalive_task.cancel()
        with suppress(asyncio.CancelledError):
            await keepalive_task


app = FastAPI(
    title="SEO Valdemoro | SEO local y desarrollo web",
    description="Desarrollo web, SEO local y posicionamiento en IA para negocios de Valdemoro.",
    version="2.0.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", name="home")
async def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=page_context(
            request,
            "SEO local y desarrollo web en Valdemoro | SEO Valdemoro",
            "SEO local, desarrollo web y posicionamiento en IA para comercios y PyMEs de Valdemoro.",
            page="home",
        ),
    )


@app.get("/servicios/{service_slug}", name="service")
async def service_page(request: Request, service_slug: str):
    service = SERVICES.get(service_slug)
    if service is None:
        return Response("Not found", status_code=404)
    return templates.TemplateResponse(
        request=request,
        name="service.html",
        context=page_context(request, f"{service['title']} | {settings.site_name}", service["description"], page="service", service=service),
    )


@app.get("/casos-exito-valdemoro", name="cases")
async def cases_page(request: Request):
    return templates.TemplateResponse(request=request, name="cases.html", context=page_context(request, f"Casos de éxito SEO local en Valdemoro | {settings.site_name}", "Cómo medimos visibilidad local, contactos y oportunidades de mejora.", page="cases"))


@app.get("/sobre-nosotros", name="about")
async def about_page(request: Request):
    return templates.TemplateResponse(request=request, name="about.html", context=page_context(request, f"Sobre {settings.site_name} | Estrategia digital en Valdemoro", "Conoce el enfoque de SEO Valdemoro para construir presencia digital local.", page="about"))


@app.get("/blog", name="blog")
async def blog_page(request: Request):
    return templates.TemplateResponse(request=request, name="blog.html", context=page_context(request, f"Blog de SEO local y GEO en Valdemoro | {settings.site_name}", "Guías prácticas para mejorar la presencia digital de negocios locales.", page="blog"))


@app.get("/health", response_model=dict[str, str], name="health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy", "message": "Web server is running"}


@app.get("/robots.txt", response_class=PlainTextResponse, name="robots")
async def robots() -> str:
    return f"User-agent: *\nAllow: /\nSitemap: {settings.site_url}/sitemap.xml\n"


@app.get("/sitemap.xml", name="sitemap")
async def sitemap() -> Response:
    urls = "".join(
        f"<url><loc>{escape(settings.site_url + path)}</loc><changefreq>monthly</changefreq></url>"
        for path in PUBLIC_PATHS
    )
    content = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(content, media_type="application/xml")


@app.get("/keepalive", response_class=PlainTextResponse, name="keepalive")
async def keepalive() -> str:
    return "OK"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
