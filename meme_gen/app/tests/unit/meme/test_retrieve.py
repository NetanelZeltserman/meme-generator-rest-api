from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from app.views.meme.retrieve import MemeRetrieve
from app.serializers.meme import MemeSerializer
from app.models import Meme
from django.http import Http404, JsonResponse
import json
from app.tests.utils import create_test_user, create_meme_template, create_meme

class TestMemeRetrieve(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = create_test_user()
        self.template = create_meme_template()
        self.meme = create_meme(self.template, "Top Text", "Bottom Text", self.user)
        self.url = reverse('meme_retrieve', kwargs={'pk': self.meme.id})

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
