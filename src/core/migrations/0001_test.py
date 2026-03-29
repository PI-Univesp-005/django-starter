import uuid
from django.db import migrations, models


def seed(apps, schema_editor):
    HealthCheck = apps.get_model("core", "HealthCheck")
    if not HealthCheck.objects.exists():
        HealthCheck.objects.create(message="Hello, Django!")


def unseed(apps, schema_editor):
    HealthCheck = apps.get_model("core", "HealthCheck")
    HealthCheck.objects.filter(message="Hello, Django!").delete()


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HealthCheck",
            fields=[
                # UUIDField with a callable default — uuid.uuid4 (no parentheses)
                # means Django calls uuid.uuid4() fresh for each new row.
                ("id", models.UUIDField(
                    primary_key=True,
                    default=uuid.uuid4,
                    editable=False,
                )),
                ("message", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"db_table": "core_healthcheck"},
        ),
        migrations.RunPython(seed, reverse_code=unseed),
    ]