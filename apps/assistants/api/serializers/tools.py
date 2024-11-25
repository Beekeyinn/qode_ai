from rest_framework import serializers

from apps.assistants.api.choices import ParameterTypeChoices, PropertyValueFormatType
from apps.assistants.models import Assistant, AssistantTool
from apps.core import test_string_function


class PropertyValueSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=ParameterTypeChoices.choices, required=True)
    format = serializers.ChoiceField(
        choices=PropertyValueFormatType.choices, required=False
    )
    description = serializers.CharField(required=True)


class ParameterSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=ParameterTypeChoices.choices, required=True)
    properties = serializers.DictField(child=PropertyValueSerializer(), required=True)
    required = serializers.ListField(child=serializers.CharField(), required=False)

    def validate(self, attrs):
        required_fields = attrs.get("required", [])
        for field in required_fields:
            if field not in attrs["properties"]:
                raise serializers.ValidationError(
                    f"'{field}' is required but not provided in properties."
                )
        return attrs


class FunctionDescriptorSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, help_text="Name of the function")
    description = serializers.CharField(help_text="Description of the the function")
    parameters = ParameterSerializer(required=True)


class AssistantToolSerializer(serializers.ModelSerializer):
    function_descriptor = FunctionDescriptorSerializer(
        required=False,
        help_text="""{
    "name": "get_delivery_date",
    "description": "Get the delivery date for a customer's order. Call this whenever you need to know the delivery date, for example when a customer asks 'Where is my package'",
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The customer's order ID."
            }
        },
        "required": ["order_id"],
        "additionalProperties": false
    }
}""",
    )
    function_name = serializers.CharField(
        help_text="Name of the function", required=False
    )
    function_logic = serializers.CharField(
        help_text="Logic of the function", required=False
    )

    class Meta:
        model = AssistantTool
        fields = [
            "tool_type",
            "function_name",
            "function_logic",
            "function_descriptor",
            "assistant",
        ]

    def validate_function_logic(self, value):
        if "import" in value:
            raise serializers.ValidationError(
                "No import statement in function is allowed."
            )
        if "pip" in value:
            raise serializers.ValidationError(
                "No pip statement in function is allowed."
            )
        if "class" in value:
            raise serializers.ValidationError(
                "No class statement in function is allowed"
            )
        return value

    def validate(self, attrs):
        if attrs["tool_type"] == "function":
            errors = {}
            if attrs.get("function_name", None) is None:
                errors["function_name"] = "This field is required."
            if attrs.get("function_logic", None) is None:
                errors["function_logic"] = "This field is required"
            if attrs.get("function_descriptor", None) is None:
                errors["function_descriptor"] = "This field is required"
            if len(errors) > 0:
                raise serializers.ValidationError(errors)
            success, error = self.test_function(
                attrs.get("function_logic"), attrs.get("function_name")
            )
            if not success:
                raise serializers.ValidationError({"function_logic": error})
            if attrs["function_name"] != attrs["function_descriptor"]["name"]:
                raise serializers.ValidationError(
                    {
                        "function_name": f"function name provided and name in function_descriptor should be same"
                    }
                )

        return super().validate(attrs)

    def test_function(self, function_logic, function_name):
        return test_string_function(function_logic, function_name)

    def create(self, validated_data):
        view = self.context.get("view", None)
        if view is None:
            raise ValueError("View must be provided in context")
        validated_data["assistant"] = Assistant.objects.get(
            id=view.kwargs["assistant_pk"]
        )
        return super().create(validated_data)
