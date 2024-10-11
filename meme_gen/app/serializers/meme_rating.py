from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from app.models import Rating, Meme

class MemeRatingSerializer(serializers.ModelSerializer):
    meme = serializers.PrimaryKeyRelatedField(queryset=Meme.objects.all())
    
    class Meta:
        model = Rating
        fields = ['meme', 'score']

    def validate_score(self, value):
        if not 1 <= value <= 5:
            raise ValidationError("Score must be between 1 and 5.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        return Rating.objects.update_or_create(
            meme=validated_data['meme'],
            user=user,
            defaults={'score': validated_data['score']}
        )[0]