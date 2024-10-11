from app.tests.utils import create_meme_templates
from rest_framework.test import APIClient
from app.models import MemeTemplate
from rest_framework import status
from django.test import TestCase
from django.urls import reverse

class MemeTemplateListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('meme_template_list')
        self.meme_templates = create_meme_templates(2)

    def test_list_meme_templates(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.meme_templates))

    def test_meme_template_content(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for index, meme_template in enumerate(self.meme_templates):
            self.assert_meme_template_data(response.data[index], meme_template)

    def assert_meme_template_data(self, response_data, expected_template):
        self.assertEqual(response_data['name'], expected_template.name)
        self.assertEqual(response_data['image_url'], expected_template.image_url)
        self.assertEqual(response_data['default_top_text'], expected_template.default_top_text)
        self.assertEqual(response_data['default_bottom_text'], expected_template.default_bottom_text)

    def test_empty_list(self):
        MemeTemplate.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
