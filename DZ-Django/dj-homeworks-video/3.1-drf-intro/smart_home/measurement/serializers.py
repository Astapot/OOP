from rest_framework import serializers

# TODO: опишите необходимые сериализаторы
class SensorSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()