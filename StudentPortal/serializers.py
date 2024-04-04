from rest_framework import serializers
from SM.models import Mark

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['subject', 'scores']