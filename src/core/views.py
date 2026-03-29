from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from core.models import HealthCheck


@require_http_methods(["GET"])
def hello(request):
    record = HealthCheck.objects.first()
    db_provider = settings.DATABASES["default"]["ENGINE"].split(".")[-1]

    return JsonResponse({
        # UUID objects are not JSON serializable — str() converts to the
        # standard "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" format.
        "id": str(record.id) if record else None,
        "message": record.message if record else "Hello, Django! (no seed record found)",
        # DjangoJSONEncoder handles datetime serialization correctly.
        "created_at": record.created_at if record else None,
        "db_backend": db_provider,
    })