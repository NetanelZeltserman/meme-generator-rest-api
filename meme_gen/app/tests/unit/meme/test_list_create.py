from django.http import QueryDict
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from unittest.mock import patch, MagicMock
from app.views.meme.list_and_create import MemeListCreateView
from app.serializers.meme import MemeSerializer, MemeCreateSerializer
from rest_framework.test import force_authenticate

User = get_user_model()

class MemeListCreateViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = MemeListCreateView.as_view()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_get_serializer_class_list(self):
        view = MemeListCreateView()
        view.request = self.factory.get('/')
        self.assertEqual(view.get_serializer_class(), MemeSerializer)

    def test_get_serializer_class_create(self):
        view = MemeListCreateView()
        view.request = self.factory.post('/')
        self.assertEqual(view.get_serializer_class(), MemeCreateSerializer)

    @patch('app.views.meme.list_and_create.MemeListCreateView.get_serializer')
    def test_create(self, mock_get_serializer):
        request_data = QueryDict('template_id=1')
        request = self.factory.post('/', data=request_data)
        request.user = self.user
        force_authenticate(request, user=self.user)

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_get_serializer.return_value = mock_serializer

        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_get_serializer.assert_called_once_with(data=request_data)
        mock_serializer.is_valid.assert_called_once()
        mock_serializer.save.assert_called_once()
