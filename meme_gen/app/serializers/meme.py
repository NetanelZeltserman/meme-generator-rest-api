from app.models import Meme
from rest_framework import serializers

class MemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = '__all__'

