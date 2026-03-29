# src/core/admin.py
from django.contrib import admin

from core.models import HealthCheck


@admin.register(HealthCheck)
class HealthCheckAdmin(admin.ModelAdmin):
    """
    Exposes HealthCheck in the Django admin panel at /admin/.
    list_display controls which columns appear in the list view.
    readonly_fields prevents accidental edits to auto-set timestamps.
    """
    list_display = ("id", "message", "created_at")
    readonly_fields = ("created_at",)