from rest_framework import serializers

class RealTimeDataSerializer(serializers.Serializer):
    dayofweek = serializers.IntegerField()
    time = serializers.TimeField()