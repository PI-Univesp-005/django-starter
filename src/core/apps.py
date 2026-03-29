from django.apps import AppConfig


class CoreConfig(AppConfig):
    # BigAutoField is already set globally in settings.py, but being explicit
    # here makes the app's behaviour self-documenting if it's ever moved to
    # another project with different defaults.
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core"