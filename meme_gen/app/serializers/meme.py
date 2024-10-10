from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from app.models import Meme, MemeTemplate

class MemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meme
        fields = '__all__'

class MemeCreateSerializer(serializers.ModelSerializer):
    template_id = serializers.IntegerField()
    top_text = serializers.CharField(required=False, allow_blank=True)
    bottom_text = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Meme
        fields = ['template_id', 'top_text', 'bottom_text']

    def validate_template_id(self, value):
        if not MemeTemplate.objects.filter(id=value).exists():
            raise ValidationError("A meme template with the given ID does not exist.")
        return value

    def create(self, validated_data):
        template = MemeTemplate.objects.get(id=validated_data.pop('template_id'))
        
        meme = Meme(
            template=template,
            top_text=validated_data.get('top_text') or template.default_top_text,
            bottom_text=validated_data.get('bottom_text') or template.default_bottom_text,
            created_by=self.context['request'].user
        )
        meme.save()

        return meme