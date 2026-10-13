import shlex

import httpx
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import WebhookEvent


def dashboard(request: HttpRequest):
    return render(
        request,
        "dashboard.html",
        {"events": WebhookEvent.objects.all()[:50], "token": settings.ROOT_TOKEN},
    )


@csrf_exempt
def receive_webhook(request: HttpRequest, token: str):
    if token != settings.ROOT_TOKEN:
        return JsonResponse({"error": "invalid webhook token"}, status=404)
    raw_headers = {
        key.removeprefix("HTTP_").replace("_", "-").lower(): value
        for key, value in request.META.items()
        if key.startswith("HTTP_")
    }
    raw_headers["content-type"] = request.content_type or ""
    event = WebhookEvent.objects.create(
        method=request.method,
        path=request.path,
        query_string=request.META.get("QUERY_STRING", ""),
        headers=raw_headers,
        body=request.body.decode("utf-8", errors="replace"),
        content_type=request.content_type or "",
        source_ip=request.META.get("REMOTE_ADDR"),
    )
    return JsonResponse({"received": True, "event_id": event.id}, status=202)


def events_api(request: HttpRequest):
    return JsonResponse({"events": [event.as_dict() for event in WebhookEvent.objects.all()[:100]]})


def replay_event(request: HttpRequest, event_id: int):
    event = get_object_or_404(WebhookEvent, id=event_id)
    target = request.POST.get("target") or request.GET.get("target")
    if not target:
        return JsonResponse({"error": "target URL is required"}, status=400)
    try:
        response = httpx.request(
            event.method, target, content=event.body.encode(), headers=event.headers, timeout=10
        )
        event.replay_count += 1
        event.save(update_fields=["replay_count"])
        return JsonResponse(
            {
                "event_id": event.id,
                "status_code": response.status_code,
                "response": response.text[:2000],
            }
        )
    except httpx.HTTPError as exc:
        return JsonResponse({"error": str(exc)}, status=502)


def curl_event(request: HttpRequest, event_id: int):
    event = get_object_or_404(WebhookEvent, id=event_id)
    target = request.GET.get("target", "http://localhost:8000/your-endpoint/")
    command = ["curl", "-X", event.method, target]
    for key, value in event.headers.items():
        command += ["-H", f"{key}: {value}"]
    if event.body:
        command += ["--data-raw", event.body]
    return JsonResponse({"command": " ".join(shlex.quote(part) for part in command)})
