from rest_framework import serializers


class TestSerializer(serializers.Serializer):
    function_logic = serializers.CharField(required=True)
    function_name = serializers.CharField(required=True)
    paramters = serializers.DictField(required=True)
