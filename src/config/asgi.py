"""
ASGI config for the Django Starter project.

ASGI stands for Asynchronous Server Gateway Interface. It is the modern
successor to WSGI, designed to support not only standard HTTP requests but
also long-lived connections like WebSockets and HTTP/2 server-sent events.

Django has supported ASGI since version 3.0. For this starter project we
are not using any async features, so this file exists primarily for
completeness and to future-proof the setup.

If you later add Django Channels (for WebSockets), or use an async view,
you would deploy with an ASGI server such as Daphne or Uvicorn instead of
Gunicorn:

    uvicorn config.asgi:application --host 0.0.0.0 --port 8000

See also: https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
