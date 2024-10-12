from app.tests.utils import create_memes, create_meme_template, create_test_user
from rest_framework.test import APITestCase
from app.models import Meme, Rating
from rest_framework import status
from django.db.models import Avg
from django.urls import reverse

class MemeTopTenRatedTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('meme_top_ten_rated')
        self.users = [create_test_user(username=f'user{i}', password=f'pass{i}') for i in range(3)]
        self.template = create_meme_template()
        self.memes = create_memes(15, self.template, self.users[0])

        for i, meme in enumerate(self.memes):
            for j, user in enumerate(self.users):
                Rating.objects.create(meme=meme, user=user, score=((i + j) % 5) + 1)

    def test_retrieve_top_ten_rated_memes(self):
        self.client.force_authenticate(user=self.users[0])

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

        top_memes = Meme.objects.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')[:10]

        for response_meme, db_meme in zip(response.data, top_memes):
            self.assertEqual(response_meme['id'], db_meme.id)
            self.assertEqual(response_meme['top_text'], db_meme.top_text)
            self.assertEqual(response_meme['bottom_text'], db_meme.bottom_text)

    def test_retrieve_nonexistent_meme(self):
        self.client.force_authenticate(user=self.users[0])
        Meme.objects.all().delete()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["custom_message"], 'No memes found.')

    def test_method_not_allowed(self):
        self.client.force_authenticate(user=self.users[0])
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
