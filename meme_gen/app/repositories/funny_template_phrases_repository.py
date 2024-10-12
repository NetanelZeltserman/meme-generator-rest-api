from django.core.exceptions import ObjectDoesNotExist
from app.models import FunnyTemplatePhrases
from random import choice

class FunnyTemplatePhrasesRepository:

    @staticmethod
    def get_random_funny_template_phrase(template_id=None):
        queryset = FunnyTemplatePhrases.objects.all()

        if template_id:
            queryset = queryset.filter(template_id=template_id)

        if not queryset.exists():
            raise ObjectDoesNotExist("No funny template phrases found.")

        return choice(queryset)