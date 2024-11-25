from rest_framework import serializers

from apps.assistants.models import AssistantFile
from apps.assistants.signal import bulk_file_signal


class AssistantFileListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        files = [AssistantFile(**item) for item in validated_data]
        bulk_files = AssistantFile.objects.bulk_create(files)
        assistant_files = AssistantFile.objects.in_bulk(
            [file.id for file in bulk_files]
        )
        bulk_file_signal.send(sender=AssistantFile, files=assistant_files)
        return bulk_files


class AssistantFileModelSerialzer(serializers.ModelSerializer):
    class Meta:
        model = AssistantFile
        fields = ["name", "file_id", "file", "assistant", "purpose"]
        read_only_fields = ("file_id",)
        list_serializer_class = AssistantFileListSerializer

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request is None:
            raise ValueError(
                f"Request object is missing from serializer({self.__class__.__name__}) context."
            )
        validated_data["user"] = request.user
        return super().create(validated_data)


class AssistantFileModelUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantFile
        fields = ["name", "file_id", "file", "assistant", "purpose"]
        read_only_fields = (
            "file_id",
            "file",
            "assistant",
            "purpose",
        )


class AssistantFileModelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantFile
        fields = ["name", "file_id", "file", "assistant", "purpose"]
        read_only_fields = (
            "file_id",
            "assistant",
        )
