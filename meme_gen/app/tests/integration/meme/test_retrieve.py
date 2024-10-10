from app.models import Meme, MemeTemplate, User
from app.serializers.meme import MemeSerializer
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class MemeRetrieveTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.template = MemeTemplate.objects.create(
            name="Test Template",
            image_url="http://example.com/template.jpg",
            default_top_text="Default Top",
            default_bottom_text="Default Bottom"
        )
        self.meme = Meme.objects.create(
            template=self.template,
            top_text="Test Top Text",
            bottom_text="Test Bottom Text",
            created_by=self.user
        )
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
