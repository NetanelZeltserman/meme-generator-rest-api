from app.tests.utils import create_meme, create_memes
from app.models import Meme, MemeTemplate, User
from app.serializers.meme import MemeSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class MemeRandomTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.template = MemeTemplate.objects.create(
            name="Test Template",
            image_url="http://example.com/template.jpg",
            default_top_text="Default Top",
            default_bottom_text="Default Bottom"
        )
        self.memes = create_memes(5, self.template, self.user)
        self.url_name = 'meme_random'
        self.url = reverse(self.url_name)

    def create_meme(self, top_text='Test Top', bottom_text='Test Bottom'):
        return Meme.objects.create(
            template=self.template,
            top_text=top_text,
            bottom_text=bottom_text,
            created_by=self.user
        )

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
