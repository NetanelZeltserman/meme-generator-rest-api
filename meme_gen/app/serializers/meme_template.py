from rest_framework import serializers
from app.models import MemeTemplate

class MemeTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemeTemplate
        fields = '__all__'
