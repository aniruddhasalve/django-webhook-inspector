from django.db import models


class WebhookEvent(models.Model):
    method = models.CharField(max_length=12)
    path = models.CharField(max_length=500)
    query_string = models.TextField(blank=True)
    headers = models.JSONField(default=dict)
    body = models.TextField(blank=True)
    content_type = models.CharField(max_length=200, blank=True)
    source_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    replay_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def as_dict(self):
        return {
            "id": self.id,
            "method": self.method,
            "path": self.path,
            "query_string": self.query_string,
            "headers": self.headers,
            "body": self.body,
            "content_type": self.content_type,
            "source_ip": self.source_ip,
            "created_at": self.created_at.isoformat(),
            "replay_count": self.replay_count,
        }
