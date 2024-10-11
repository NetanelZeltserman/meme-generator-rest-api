from django.db.models import ObjectDoesNotExist
from django.db.models import Count
from app.models import Meme
from random import randint

class MemeRepository:

    @staticmethod
    def get_random_meme():
        meme_count = Meme.objects.aggregate(count=Count('id'))['count']

        if not meme_count:
            raise ObjectDoesNotExist("No memes found.")

        random_index = randint(0, meme_count - 1)
        return Meme.objects.all()[random_index]