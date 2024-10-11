from app.tests.utils import create_test_user, create_meme_template, create_meme
from app.serializers.meme import MemeSerializer
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class MemeRetrieveTestCase(APITestCase):
    def setUp(self):
        self.user = create_test_user()
        self.template = create_meme_template()
        self.meme = create_meme(self.template, "Test Top Text", "Test Bottom Text", self.user)
        self.url_name = 'meme_retrieve'
        self.url = reverse(self.url_name, kwargs={'pk': self.meme.pk})

    def test_retrieve_existing_meme(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MemeSerializer(self.meme).data)

    def test_retrieve_non_existent_meme(self):
        self.client.force_authenticate(user=self.user)
        non_existent_url = reverse(self.url_name, kwargs={'pk': 9999})
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_method_not_allowed(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
