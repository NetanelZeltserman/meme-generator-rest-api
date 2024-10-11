from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from app.views.meme.rate import MemeRateView
from unittest.mock import patch, MagicMock
from rest_framework import status
from django.test import TestCase
from app.tests.utils import create_test_user, create_meme_template, create_meme

class MemeRateViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = create_test_user()
        self.template = create_meme_template(name='Test Template')
        self.meme = create_meme(template=self.template, top_text='Top', bottom_text='Bottom', user=self.user)
        self.view = MemeRateView.as_view()

    @patch('app.views.meme.rate.MemeRateView.get_serializer')
    @patch('app.exceptions.factory.ExceptionsFactory.handle')
    def test_invalid_data(self, mock_handle_exception, mock_get_serializer):
        mock_serializer = MagicMock()
        mock_serializer.is_valid.side_effect = ValidationError("Invalid score")
        mock_get_serializer.return_value = mock_serializer

        mock_handle_exception.return_value = Response(
            {"error": "Custom invalid score exception"},
            status=status.HTTP_400_BAD_REQUEST
        )

        data = {'meme': self.meme.id, 'score': 6} # Invalid score
        request = self.factory.post('/meme/rate/', data)
        force_authenticate(request, user=self.user)

        response = self.view(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Custom invalid score exception"})
        mock_handle_exception.assert_called_once()

    @patch('app.views.meme.rate.MemeRateView.get_serializer')
    @patch('app.exceptions.factory.ExceptionsFactory.handle')
    def test_exception_handling(self, mock_exception_handler, mock_get_serializer):
        mock_serializer = MagicMock()
        mock_serializer.is_valid.side_effect = Exception("Test exception")
        mock_get_serializer.return_value = mock_serializer

        mock_exception_handler.return_value = Response(
            {'error': 'Test error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

        data = {'meme': self.meme.id, 'score': 5}
        request = self.factory.post('/meme/rate/', data)
        force_authenticate(request, user=self.user)

        response = self.view(request)

        mock_exception_handler.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {'error': 'Test error'})
