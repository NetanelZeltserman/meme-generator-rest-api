from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch, MagicMock
from app.views.meme.retrieve import MemeRetrieve
from app.serializers.meme import MemeSerializer
from app.models import Meme, MemeTemplate
from django.http import Http404, JsonResponse
import json

class TestMemeRetrieve(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test_username', password='test_pass')
        self.meme = self.create_mock_meme()
        self.url = reverse('meme_retrieve', kwargs={'pk': self.meme.id})

    @staticmethod
    def create_mock_meme():
        meme = MagicMock(spec=Meme)
        meme.id = 1
        meme.template = MagicMock(spec=MemeTemplate)
        meme.top_text = "Top Text"
        meme.bottom_text = "Bottom Text"
        meme.created_by = User.objects.first()
        return meme

    def test_retrieve_meme_success(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)

        with patch.object(MemeRetrieve, 'get_object', return_value=self.meme):
            response = MemeRetrieve.as_view()(request, pk=self.meme.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, MemeSerializer(self.meme).data)

    def test_retrieve_nonexistent_meme(self):
        with patch('app.views.meme.retrieve.Meme.objects.get', side_effect=Meme.DoesNotExist):
            view = MemeRetrieve()
            view.kwargs = {'pk': 9999}
            with self.assertRaises(Http404):
                view.retrieve(self.factory.get(self.url))

    def test_retrieve_meme_exception_handling(self):
        error_response = JsonResponse({'error': 'Test error'}, status=404)
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)

        with patch('app.views.meme.retrieve.ExceptionsFactory.handle', return_value=error_response), \
             patch.object(MemeRetrieve, 'get_object', side_effect=Http404("Test exception")):
            response = MemeRetrieve.as_view()(request, pk=self.meme.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {'error': 'Test error'})
