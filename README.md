# SEO Valdemoro

A maintainable FastAPI website for SEO Valdemoro, a local digital services studio serving businesses in Valdemoro, Madrid.

## Features

- FastAPI application with Jinja2 templates
- Responsive multi-page layout for local SEO, web development, and GEO services
- Static CSS served from `/static`
- Health check endpoint at `/health`
- Keep-alive endpoint at `/keepalive`
- `robots.txt` and `sitemap.xml` endpoints
- Phone and WhatsApp contact paths
- Optional Render keep-alive support
- Automated smoke tests for public routes and SEO endpoints

The site is intentionally contact-first: visitors can call `615 09 68 57` or open a prefilled WhatsApp conversation. There is no form, email collection, or SMTP integration.

## Requirements

- Python 3.10 or newer

## Local setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the development server:

```bash
python3 main.py
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

Run the test suite:

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Renders the main website |
| `GET` | `/servicios/{service_slug}` | Renders a focused service page |
| `GET` | `/casos-exito-valdemoro` | Displays the measurement framework for case studies |
| `GET` | `/sobre-nosotros` | Displays the working approach and local coverage |
| `GET` | `/blog` | Displays the resource archive |
| `GET` | `/health` | Returns the application health status |
| `GET` | `/keepalive` | Returns `OK` for monitoring and keep-alive requests |
| `GET` | `/robots.txt` | Provides crawler instructions |
| `GET` | `/sitemap.xml` | Lists the public pages |

## Project structure

```text
.
├── main.py
├── pyproject.toml
├── render.yaml
├── requirements.txt
├── requirements-dev.txt
├── static/
│   └── site.css
└── templates/
    ├── about.html
    ├── base.html
    ├── blog.html
    ├── cases.html
    ├── index.html
    └── service.html
└── tests/
    └── test_app.py
```

The backend keeps configuration, content, route registration, metadata, sitemap generation, and the Render keep-alive lifecycle in one small module with explicit boundaries. Templates share `templates/base.html`; service pages are generated from the service catalog instead of duplicating route logic.

## Render keep-alive

When deployed on Render, set `RENDER_EXTERNAL_URL` to the public service URL. The application will periodically request `/keepalive`.

The interval can be customized with `KEEPALIVE_INTERVAL` in seconds. It defaults to `270` seconds.

`render.yaml` contains the recommended Render service and start command. Set `SITE_URL` to the final public HTTPS URL so canonical tags, `robots.txt`, the sitemap, and structured data point to the correct origin.

## Customization

Update the copy and metadata in `templates/index.html`, and adjust the visual design in `static/site.css` to match the business or brand.

The default site identity is `SEO Valdemoro`. It and the public URL can be configured with `SITE_NAME` and `SITE_URL`. Replace the placeholder NAP information in `templates/base.html` before using the site in production.

## Contact

The public contact phone is `615 09 68 57`, and WhatsApp uses the international number `+34 615 09 68 57`. WhatsApp links include a short prefilled message to reduce friction.