"""FastAPI website for a local digital services studio in Valdemoro."""

import os
import smtplib
import threading
import time
import urllib.request
from email.message import EmailMessage
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="SEO Valdemoro | SEO local y desarrollo web", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

SITE_URL = os.environ.get("SITE_URL", "http://localhost:8000").rstrip("/")
SITE_NAME = os.environ.get("SITE_NAME", "SEO Valdemoro")
CONTACT_EMAIL = "angel.maturana@gmail.com"
CONTACT_PHONE = "615 09 68 57"
CONTACT_PHONE_E164 = "+34615096857"
WHATSAPP_URL = "https://wa.me/34615096857?text=Hola%20SEO%20Valdemoro%2C%20quiero%20mejorar%20la%20presencia%20digital%20de%20mi%20negocio."

SERVICES = {
    "desarrollo-web-valdemoro": {
        "title": "Desarrollo web móvil en Valdemoro",
        "short_title": "Web móvil",
        "eyebrow": "01 / Web que trabaja",
        "intro": "Una web rápida, clara y pensada para convertir visitas desde el móvil en conversaciones reales.",
        "description": "Diseñamos sitios web mobile-first para comercios y pequeñas empresas de Valdemoro, con una arquitectura sencilla, contenidos útiles y llamadas a la acción visibles.",
        "points": [
            "Arquitectura mobile-first y navegación sin fricción.",
            "Páginas preparadas para crecer con nuevos servicios.",
            "Contenido orientado a llamadas, formularios y visitas.",
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

NAV_ITEMS = [
    ("Inicio", "/"),
    ("Servicios", "/#servicios"),
    ("Casos", "/casos-exito-valdemoro"),
    ("Nosotros", "/sobre-nosotros"),
    ("Blog", "/blog"),
]


def page_context(request: Request, title: str, description: str, **values: object) -> dict[str, object]:
    """Build the shared context used by every page template."""
    path = request.url.path
    return {
        "site_name": SITE_NAME,
        "site_url": SITE_URL,
        "canonical_url": f"{SITE_URL}{path}",
        "page_title": title,
        "page_description": description,
        "nav_items": NAV_ITEMS,
        "services": SERVICES,
        "contact_email": CONTACT_EMAIL,
        "contact_phone": CONTACT_PHONE,
        "contact_phone_e164": CONTACT_PHONE_E164,
        "whatsapp_url": WHATSAPP_URL,
        **values,
    }


def send_audit_email(business_name: str, email: str, phone: str) -> bool:
    """Send an audit notification when SMTP credentials are configured."""
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    if not all((smtp_host, smtp_user, smtp_password)):
        return False

    message = EmailMessage()
    message["Subject"] = f"Nueva solicitud de auditoría: {business_name}"
    message["From"] = os.environ.get("SMTP_FROM", smtp_user)
    message["To"] = CONTACT_EMAIL
    message.set_content(
        "Nueva solicitud de auditoría SEO Valdemoro\n\n"
        f"Negocio: {business_name}\nEmail: {email}\nTeléfono/WhatsApp: {phone or 'No indicado'}\n"
    )
    port = int(os.environ.get("SMTP_PORT", "587"))
    with smtplib.SMTP(smtp_host, port, timeout=15) as smtp:
        smtp.starttls()
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(message)
    return True


def keep_alive_ping() -> None:
    """Ping the public service periodically when deployed on Render."""
    time.sleep(30)

    external_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not external_url:
        print("[Keep-Alive] RENDER_EXTERNAL_URL not set - skipping keep-alive (local mode)")
        return

    ping_url = f"{external_url.rstrip('/')}/keepalive"
    try:
        interval = max(60, int(os.environ.get("KEEPALIVE_INTERVAL", "270")))
    except ValueError:
        interval = 270
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
    """Render the conversion-focused home page."""
    context = page_context(
        request,
        "SEO local y desarrollo web en Valdemoro | SEO Valdemoro",
        "Diseño web, SEO local y posicionamiento en IA para comercios y PyMEs de Valdemoro.",
        page="home",
    )
    return templates.TemplateResponse(request=request, name="index.html", context=context)


@app.get("/servicios/{service_slug}")
async def service_page(request: Request, service_slug: str):
    """Render one of the focused service pages."""
    service = SERVICES.get(service_slug)
    if service is None:
        return Response("Not found", status_code=404)
    context = page_context(
        request,
        f"{service['title']} | {SITE_NAME}",
        service["description"],
        page="service",
        service=service,
    )
    return templates.TemplateResponse(request=request, name="service.html", context=context)


@app.get("/casos-exito-valdemoro")
async def cases_page(request: Request):
    context = page_context(
        request,
        f"Casos de éxito de SEO local en Valdemoro | {SITE_NAME}",
        "Un marco transparente para medir visibilidad local, contactos y oportunidades de mejora.",
        page="cases",
    )
    return templates.TemplateResponse(request=request, name="cases.html", context=context)


@app.get("/sobre-nosotros")
async def about_page(request: Request):
    context = page_context(
        request,
        f"Sobre {SITE_NAME} | Estrategia digital en Valdemoro",
        "Conoce nuestro enfoque de trabajo para construir presencia digital local con claridad y criterio.",
        page="about",
    )
    return templates.TemplateResponse(request=request, name="about.html", context=context)


@app.get("/auditoria-gratuita-valdemoro")
async def audit_page(request: Request):
    context = page_context(
        request,
        f"Auditoría digital gratuita en Valdemoro | {SITE_NAME}",
        "Solicita una revisión inicial de tu web, presencia local y oportunidades de captación.",
        page="audit",
    )
    return templates.TemplateResponse(request=request, name="audit.html", context=context)


@app.post("/auditoria-gratuita-valdemoro")
def submit_audit(
    request: Request,
    business_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
):
    """Send the audit request when configured and expose WhatsApp as fallback."""
    safe_business_name = business_name.strip()[:120]
    safe_email = email.strip()[:160]
    safe_phone = phone.strip()[:40]
    email_sent = False
    email_error = False
    try:
        email_sent = send_audit_email(safe_business_name, safe_email, safe_phone)
    except (OSError, smtplib.SMTPException, ValueError):
        email_error = True
    context = page_context(
        request,
        f"Solicitud recibida | {SITE_NAME}",
        "Tu solicitud de auditoría digital ha sido recibida.",
        page="audit",
        submitted=True,
        submitted_name=safe_business_name,
        submitted_email=safe_email,
        submitted_phone=safe_phone,
        email_sent=email_sent,
        email_error=email_error,
    )
    return templates.TemplateResponse(request=request, name="audit.html", context=context)


@app.get("/blog")
async def blog_page(request: Request):
    context = page_context(
        request,
        f"Blog de SEO local y GEO en Valdemoro | {SITE_NAME}",
        "Guías prácticas para mejorar la presencia digital de negocios locales.",
        page="blog",
    )
    return templates.TemplateResponse(request=request, name="blog.html", context=context)


@app.get("/robots.txt")
async def robots(request: Request):
    content = f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"
    return PlainTextResponse(content)


@app.get("/sitemap.xml")
async def sitemap(request: Request):
    paths = ["/", "/casos-exito-valdemoro", "/sobre-nosotros", "/auditoria-gratuita-valdemoro", "/blog"]
    paths.extend(f"/servicios/{slug}" for slug in SERVICES)
    urls = "".join(f"<url><loc>{SITE_URL}{path}</loc><changefreq>monthly</changefreq></url>" for path in paths)
    content = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(content, media_type="application/xml")


@app.get("/keepalive")
async def keepalive() -> PlainTextResponse:
    """Endpoint used by the internal keep-alive request and monitors."""
    return PlainTextResponse("OK", status_code=200)


if __name__ == "__main__":
    import uvicorn

    print("Starting web server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
