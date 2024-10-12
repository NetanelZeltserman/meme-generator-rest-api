from django.db.models import ObjectDoesNotExist, Count, Avg
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

    @staticmethod
    def get_top_rated_memes(limit=10):
        top_memes = Meme.objects.annotate(
            avg_rating=Avg('ratings__score')
        ).order_by('-avg_rating')[:limit]
        
        if not top_memes:
            raise ObjectDoesNotExist("No memes found.")
        
        return top_memes