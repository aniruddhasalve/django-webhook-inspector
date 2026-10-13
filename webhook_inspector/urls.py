from django.urls import path

from inspector_app import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("hooks/<slug:token>/", views.receive_webhook, name="receive_webhook"),
    path("api/events/", views.events_api, name="events_api"),
    path("api/events/<int:event_id>/replay/", views.replay_event, name="replay_event"),
    path("api/events/<int:event_id>/curl/", views.curl_event, name="curl_event"),
]
