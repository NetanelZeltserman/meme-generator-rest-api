from app.serializers.meme_template import MemeTemplateSerializer
from app.models import FunnyTemplatePhrases
from rest_framework import serializers

class FunnyTemplatePhrasesSerializer(serializers.ModelSerializer):
    template = MemeTemplateSerializer()

    class Meta:
        model = FunnyTemplatePhrases
        fields = '__all__'
