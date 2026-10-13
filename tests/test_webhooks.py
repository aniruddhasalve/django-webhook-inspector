import json

import pytest

from inspector_app.models import WebhookEvent


@pytest.mark.django_db
def test_webhook_is_captured(client):
    response = client.post(
        "/hooks/dev-webhook-token/?source=stripe",
        data=json.dumps({"type": "payment.succeeded"}),
        content_type="application/json",
        HTTP_X_SIGNATURE="abc",
    )
    assert response.status_code == 202
    event = WebhookEvent.objects.get()
    assert event.method == "POST"
    assert event.query_string == "source=stripe"
    assert event.headers["x-signature"] == "abc"
    assert json.loads(event.body)["type"] == "payment.succeeded"


@pytest.mark.django_db
def test_invalid_token_is_not_stored(client):
    response = client.post("/hooks/wrong-token/", data="{}", content_type="application/json")
    assert response.status_code == 404
    assert WebhookEvent.objects.count() == 0


@pytest.mark.django_db
def test_events_api_returns_captured_event(client):
    client.post("/hooks/dev-webhook-token/", data="hello", content_type="text/plain")
    response = client.get("/api/events/")
    assert response.status_code == 200
    assert response.json()["events"][0]["body"] == "hello"
