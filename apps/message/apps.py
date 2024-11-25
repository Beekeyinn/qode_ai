from django.apps import AppConfig


class MessageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.message"

    def ready(self) -> None:
        import apps.message.signals

        return super().ready()
