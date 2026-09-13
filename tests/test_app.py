from fastapi.testclient import TestClient

from main import PUBLIC_PATHS, app, settings


client = TestClient(app)


def test_public_pages_render():
    paths = [
        "/",
        "/servicios/desarrollo-web-valdemoro",
        "/servicios/seo-local-google-maps-valdemoro",
        "/servicios/posicionamiento-ia-chatgpt-valdemoro",
        "/servicios/pack-digital-valdemoro",
        "/casos-exito-valdemoro",
        "/sobre-nosotros",
        "/blog",
    ]
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200
        assert "SEO Valdemoro" in response.text


def test_unknown_service_returns_not_found():
    assert client.get("/servicios/no-existe").status_code == 404


def test_contact_and_seo_endpoints():
    home = client.get("/").text
    assert settings.phone in home
    assert settings.whatsapp_url in home
    assert 'type="application/ld+json"' in home
    assert "FAQPage" in home
    assert client.get("/robots.txt").text.endswith("/sitemap.xml\n")
    assert client.get("/sitemap.xml").text.count("<url>") == len(PUBLIC_PATHS)


def test_health_and_keepalive():
    assert client.get("/health").json()["status"] == "healthy"
    assert client.get("/keepalive").text == "OK"
