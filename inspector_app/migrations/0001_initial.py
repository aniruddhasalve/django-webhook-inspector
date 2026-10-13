from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="WebhookEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("method", models.CharField(max_length=12)),
                ("path", models.CharField(max_length=500)),
                ("query_string", models.TextField(blank=True)),
                ("headers", models.JSONField(default=dict)),
                ("body", models.TextField(blank=True)),
                ("content_type", models.CharField(blank=True, max_length=200)),
                ("source_ip", models.GenericIPAddressField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("replay_count", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["-created_at"]},
        )
    ]
