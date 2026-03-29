# src/core/urls.py
#
# Each app owns its URL configuration. The project's root urls.py includes
# this file with include(), keeping routing modular — adding or removing the
# core app from the project is a one-line change in config/urls.py.

from django.urls import path

from core.views import hello

app_name = "core"  # Enables URL namespacing: reverse("core:hello")

urlpatterns = [
    path("", hello, name="hello"),
]