# Django Webhook Inspector

**A Docker-first local webhook inbox for inspecting, replaying, and exporting HTTP requests.**

Stop guessing what Stripe, GitHub, Shopify, or your own service sent. Point a webhook at one local endpoint and inspect the full request in a browser.

## Quickstart

```bash
git clone https://github.com/aniruddhasalve/django-webhook-inspector.git
cd django-webhook-inspector
docker compose up --build
```

Open **http://localhost:8000**.

Send a test webhook:

```bash
curl -X POST http://localhost:8000/hooks/dev-webhook-token/ \\
  -H 'content-type: application/json' \\
  -H 'x-signature: demo-signature' \\
  -d '{"event":"payment.succeeded","id":"evt_demo_123"}'
```

The dashboard shows the request, headers, payload, query string, source IP, and replay count.

## API

| Endpoint | Purpose |
|---|---|
| `POST /hooks/<token>/` | Capture any HTTP request |
| `GET /api/events/` | List captured events as JSON |
| `GET /api/events/<id>/curl/` | Export an event as a cURL command |
| `POST /api/events/<id>/replay/` | Replay to a supplied `target` URL |
| `GET /` | Browser dashboard |

Replay example:

```bash
curl -X POST 'http://localhost:8000/api/events/1/replay/?target=http://host.docker.internal:9000/webhook/'
```

## Security and scope

This tool is intended for local development. It stores request bodies and headers, so do not expose it publicly without adding authentication, retention limits, redaction, and a proper secret. The token is configurable as `ROOT_TOKEN` in Django settings.

## Development

```bash
pip install -e '.[dev]'
python manage.py migrate
pytest -q
ruff check .
```

## Roadmap

- Search and filters in the dashboard
- Payload/header redaction rules
- HMAC signature verification helpers
- Event tags and notes
- Redis-backed asynchronous forwarding
- Public tunnel adapter
- PostgreSQL production profile

MIT licensed. Contributions welcome.
