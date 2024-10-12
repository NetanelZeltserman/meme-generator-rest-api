from app.tests.utils import create_test_user, create_meme_template, create_memes
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class MemeTopTenRatedViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('meme_top_ten_rated')
        self.user = create_test_user()
        self.client.force_authenticate(user=self.user)
        self.template = create_meme_template()

    @patch('app.repositories.meme_repository.MemeRepository.get_top_rated_memes')
    def test_list_top_rated_memes_success(self, mock_get_top_rated_memes):
        mock_memes = create_memes(10, self.template, self.user)
        mock_get_top_rated_memes.return_value = mock_memes

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
        mock_get_top_rated_memes.assert_called_once_with(limit=10)

    def test_list_top_rated_memes_unauthenticated(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('app.repositories.meme_repository.MemeRepository.get_top_rated_memes')
    @patch('app.exceptions.factory.ExceptionsFactory.handle')
    def test_list_top_rated_memes_exception(self, mock_handle_exception, mock_get_top_rated_memes):
        mock_get_top_rated_memes.side_effect = Exception("Test exception")
        mock_handle_exception.return_value = Response(
            {"error": "Test error"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {"error": "Test error"})
        mock_get_top_rated_memes.assert_called_once_with(limit=10)
        mock_handle_exception.assert_called_once()
