from app.tests.utils import create_meme_template, create_memes, create_test_user
from app.serializers.meme import MemeSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from app.models import Meme

class MemeRandomTestCase(APITestCase):
    def setUp(self):
        self.user = create_test_user()
        self.template = create_meme_template()
        self.memes = create_memes(5, self.template, self.user)
        self.url_name = 'meme_random'
        self.url = reverse(self.url_name)

    def test_retrieve_existing_meme(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data, [MemeSerializer(meme).data for meme in self.memes])

    def test_retrieve_nonexistent_meme(self):
        self.client.force_authenticate(user=self.user)
        Meme.objects.all().delete()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["custom_message"], 'No memes found.')

    def test_method_not_allowed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
