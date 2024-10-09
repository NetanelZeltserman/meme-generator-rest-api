from django.test import TestCase
from unittest.mock import patch, MagicMock
from app.views.meme_template.list import MemeTemplateList
from app.models import MemeTemplate
from app.serializers.meme_template import MemeTemplateSerializer

class TestMemeTemplateList(TestCase):
    def setUp(self):
        self.view = MemeTemplateList()

    def test_queryset_is_meme_template(self):
        self.assertEqual(self.view.queryset.model, MemeTemplate)

    def test_serializer_class_is_meme_template_serializer(self):
        self.assertEqual(self.view.serializer_class, MemeTemplateSerializer)

    @patch('app.views.meme_template.list.MemeTemplateList.list')
    def test_get_method_calls_list(self, mock_list):
        mock_request = MagicMock()
        mock_args = MagicMock()
        mock_kwargs = MagicMock()

        self.view.get(mock_request, *mock_args, **mock_kwargs)

        mock_list.assert_called_once_with(mock_request, *mock_args, **mock_kwargs)
