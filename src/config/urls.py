"""
URL configuration for the Django Starter project.

How Django routing works:
    When a request arrives, Django reads this file (the ROOT_URLCONF) and
    checks each pattern in `urlpatterns` from top to bottom. The first
    pattern that matches the request path wins, and Django calls the
    corresponding view function.

    A "path" is Django's URL pattern helper. An empty string "" matches the
    root URL ("/"). Named groups and converters can be added as the project grows.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django's built-in admin panel — available at /admin/
    path("admin/", admin.site.urls),
    # Include URL patterns from the "core" app. This allows us to keep
    # app-specific URLs organized within the app itself.
    path("", include("core.urls")),
]
