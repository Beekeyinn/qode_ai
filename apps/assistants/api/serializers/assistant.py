from rest_framework import serializers

from apps.assistants.models import Assistant


class AssistantModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "model",
            "is_global",
        ]


class AssistantModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = [
            "id",
            "name",
            "instructions",
            "description",
            "assistant_id",
            "user",
            "model",
            "is_global",
        ]
        read_only_fields = ("id", "assistant_id", "user")

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request is None:
            raise ValueError(
                f"Request is needed in context parameter of serializer {self.__class__.__name__}"
            )
        validated_data["user"] = request.user
        return super().create(validated_data)


class AssistantModelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = [
            "id",
            "name",
            "description",
            "model",
            "is_global",
            "instructions",
        ]
        read_only_fields = ("instructions",)
