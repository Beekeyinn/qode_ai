import uuid

from django.db import models


class ExtraFieldsModelsMixin(models.Model):
    id = models.UUIDField(verbose_name="ID", default=uuid.uuid4, primary_key=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
