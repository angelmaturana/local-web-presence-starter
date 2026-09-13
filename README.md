# Local Web Presence Starter

A FastAPI website for a local digital services studio serving businesses in Valdemoro, Madrid.

## Features

- FastAPI application with Jinja2 templates
- Responsive multi-page layout for local SEO, web development, and GEO services
- Static CSS served from `/static`
- Health check endpoint at `/health`
- Keep-alive endpoint at `/keepalive`
- Audit request form at `/auditoria-gratuita-valdemoro`
- `robots.txt` and `sitemap.xml` endpoints
- Phone and WhatsApp contact paths
- SMTP-backed audit notifications
- Optional Render keep-alive support

## Requirements

- Python 3.9 or newer

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

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Renders the main website |
| `GET` | `/servicios/{service_slug}` | Renders a focused service page |
| `GET` | `/casos-exito-valdemoro` | Displays the measurement framework for case studies |
| `GET` | `/sobre-nosotros` | Displays the working approach and local coverage |
| `GET` | `/auditoria-gratuita-valdemoro` | Displays the audit request form |
| `POST` | `/auditoria-gratuita-valdemoro` | Acknowledges an audit form submission |
| `GET` | `/blog` | Displays the resource archive |
| `GET` | `/health` | Returns the application health status |
| `GET` | `/keepalive` | Returns `OK` for monitoring and keep-alive requests |
| `GET` | `/robots.txt` | Provides crawler instructions |
| `GET` | `/sitemap.xml` | Lists the public pages |

## Project structure

```text
.
├── main.py
├── requirements.txt
├── static/
│   └── site.css
└── templates/
    ├── about.html
    ├── audit.html
    ├── base.html
    ├── blog.html
    ├── cases.html
    ├── index.html
    └── service.html
```

## Render keep-alive

When deployed on Render, set `RENDER_EXTERNAL_URL` to the public service URL. The application will periodically request `/keepalive`.

The interval can be customized with `KEEPALIVE_INTERVAL` in seconds. It defaults to `270` seconds.

## Customization

Update the copy and metadata in `templates/index.html`, and adjust the visual design in `static/site.css` to match the business or brand.

The default site identity is `SEO Valdemoro`. It and the public URL can be configured with `SITE_NAME` and `SITE_URL`. Replace the placeholder NAP information in `templates/base.html` and connect the audit form to an email or CRM service before using it in production.

## Contact and email delivery

The public contact phone is `615 09 68 57`, and WhatsApp uses the international number `+34 615 09 68 57`. Audit requests are delivered to `angel.maturana@gmail.com` when SMTP is configured. WhatsApp links include a short prefilled message to reduce friction.

Set these Render environment variables for email delivery:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-sending-gmail-address@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM=your-sending-gmail-address@gmail.com
```

For Gmail, use an App Password on an account with two-step verification enabled. Do not commit the password. If SMTP is not configured or fails, the form clearly directs the visitor to WhatsApp instead of reporting a false success.