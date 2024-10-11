from app.tests.utils import create_test_user, create_meme_template, create_meme
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from app.models import Rating

class MemeRatingIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_test_user()
        self.template = create_meme_template()
        self.meme = create_meme(template=self.template, top_text='Top', bottom_text='Bottom', user=self.user)
        self.url = reverse('meme_rate')

    def test_rate_meme_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'meme': self.meme.id,
            'score': 4
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().score, 4)

    def test_rate_meme_unauthenticated(self):
        data = {
            'meme': self.meme.id,
            'score': 4
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Rating.objects.count(), 0)

    def test_rate_meme_invalid_score(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'meme': self.meme.id,
            'score': 6
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rating.objects.count(), 0)

    def test_rate_meme_nonexistent_meme(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'meme': 9999,
            'score': 4
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rating.objects.count(), 0)

    def test_update_existing_rating(self):
        self.client.force_authenticate(user=self.user)
        Rating.objects.create(user=self.user, meme=self.meme, score=3)

        data = {
            'meme': self.meme.id,
            'score': 5
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().score, 5)

    def test_rate_meme_missing_data(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'meme': self.meme.id,
            # Missing 'score'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rating.objects.count(), 0)
