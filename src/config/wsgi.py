"""
WSGI config for the Django Starter project.

WSGI stands for Web Server Gateway Interface. It is the standard Python
protocol that defines how a web server (e.g. Gunicorn, uWSGI, or Apache
with mod_wsgi) communicates with a Python web application.

Think of it as a contract: any WSGI-compatible server can run any
WSGI-compatible application — including Django. The development server
(`manage.py runserver`) also uses WSGI internally.

This file exposes a module-level variable called `application`. When a
production web server starts, it imports this file and calls `application`
with each incoming request.

For the development server (`manage.py runserver`) you never need to touch
this file. It becomes relevant when you deploy to production with Gunicorn:

    gunicorn config.wsgi:application

See also: https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
