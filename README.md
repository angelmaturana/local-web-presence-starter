# Local Web Presence Starter

A lightweight FastAPI starter for a clear, responsive local-business website.

## Features

- FastAPI application with Jinja2 templates
- Responsive single-page layout
- Static CSS served from `/static`
- Health check endpoint at `/health`
- Keep-alive endpoint at `/keepalive`
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
| `GET` | `/health` | Returns the application health status |
| `GET` | `/keepalive` | Returns `OK` for monitoring and keep-alive requests |

## Project structure

```text
.
├── main.py
├── requirements.txt
├── static/
│   └── site.css
└── templates/
    └── index.html
```

## Render keep-alive

When deployed on Render, set `RENDER_EXTERNAL_URL` to the public service URL. The application will periodically request `/keepalive`.

The interval can be customized with `KEEPALIVE_INTERVAL` in seconds. It defaults to `270` seconds.

## Customization

Update the copy and metadata in `templates/index.html`, and adjust the visual design in `static/site.css` to match the business or brand.