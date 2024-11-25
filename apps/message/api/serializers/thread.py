from rest_framework import serializers

from apps.message.models import Thread


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ("id", "assistant", "user", "name")
        read_only_fields = (
            "id",
            "assistant",
            "user",
        )
