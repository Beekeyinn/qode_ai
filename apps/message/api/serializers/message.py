from rest_framework import serializers

from apps.message.models import Message, Thread
from apps.message.types import RoleChoices


class MessageSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(RoleChoices.choices, default=RoleChoices.USER)

    class Meta:
        model = Message
        fields = (
            "message",
            "role",
        )

    def create(self, validated_data):
        view = self.context.get("view", None)
        if view is None:
            raise ValueError("View must be specified in context parameter")
        validated_data["thread"] = Thread.objects.get(id=view.kwargs["thread_pk"])
        return super().create(validated_data)


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("message",)
