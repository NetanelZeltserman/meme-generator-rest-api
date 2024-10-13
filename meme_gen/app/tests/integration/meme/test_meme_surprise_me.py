from app.repositories.funny_template_phrases_repository import FunnyTemplatePhrasesRepository
from app.models import FunnyTemplatePhrases
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from app.tests.utils import (
    create_funny_template_phrases_list,
    create_test_user,
    create_meme_template
)

class MemeSurpriseMeViewTests(APITestCase):
    def setUp(self):
        self.user = create_test_user()
        self.template = create_meme_template()
        create_funny_template_phrases_list(self.template, 2)

        self.url = reverse('meme_surprise_me')
        self.url_with_template_name = 'meme_surprise_me_with_template'
        self.url_with_template = reverse(self.url_with_template_name, kwargs={'template_id': self.template.id})

    def test_surprise_me_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_surprise_me_with_nonexistent_template(self):
        self.client.force_authenticate(user=self.user)
        url_with_nonexistent_template = reverse(self.url_with_template_name, kwargs={'template_id': 9999})
        response = self.client.get(url_with_nonexistent_template)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_surprise_me_no_phrases(self):
        FunnyTemplatePhrases.objects.all().delete()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(FunnyTemplatePhrasesRepository, 'get_random_funny_template_phrase')
    def test_surprise_me_database_error(self, mock_get_random):
        mock_get_random.side_effect = Exception('Database connection error')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.content.decode())

    @patch('app.services.image_generator.funny_phrases_meme_image.FunnyPhrasesMemeImageGenerator.get_image')
    def test_surprise_me_authenticated(self, mock_get_image):
        mock_get_image.return_value = 'http://example.com/media/memes/meme_1.png'

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_valid_funny_phrase_response(response.data)
        mock_get_image.assert_called_once()

    @patch('app.services.image_generator.funny_phrases_meme_image.FunnyPhrasesMemeImageGenerator.get_image')
    def test_surprise_me_authenticated_with_template(self, mock_get_image):
        mock_get_image.return_value = 'http://example.com/media/memes/meme_2.png'

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url_with_template)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._assert_valid_funny_phrase_response(response.data)
        mock_get_image.assert_called_once()


    def _assert_valid_funny_phrase_response(self, data):
        expected_keys = ['top_phrase', 'bottom_phrase', 'template', 'image_url']

        for key in expected_keys:
            self.assertIn(key, data, f"'{key}' is missing from the response")

    def _assert_template_attributes(self, template_data):
        expected_attributes = [
            'id', 'name', 'image_url', 'default_top_text', 'default_bottom_text'
        ]
        for attr in expected_attributes:
            self.assertEqual(template_data[attr], getattr(self.template, attr))
