from app.services.image_generator.funny_phrases_meme_image import FunnyPhrasesMemeImageGenerator
from app.services.image_generator.base import ImageConfig
from unittest.mock import patch, MagicMock
from app.models import FunnyTemplatePhrases
from PIL import Image, ImageDraw, ImageFont
from django.test import TestCase

class TestFunnyPhrasesMemeImageGenerator(TestCase):

    def setUp(self):
        self.generator = FunnyPhrasesMemeImageGenerator()
        self.mock_funny_template_phrases = MagicMock(spec=FunnyTemplatePhrases)
        self.mock_funny_template_phrases.id = 1
        self.mock_funny_template_phrases.top_phrase = "Top Text"
        self.mock_funny_template_phrases.bottom_phrase = "Bottom Text"
        self.mock_funny_template_phrases.template.image_url = "http://example.com/image.jpg"

    @patch('app.services.image_generator.funny_phrases_meme_image.default_storage')
    def test_get_image_existing(self, mock_storage):
        mock_storage.exists.return_value = True
        self.generator.get_file_url = MagicMock(return_value="http://example.com/meme_1.png")

        result = self.generator.get_image(self.mock_funny_template_phrases)

        mock_storage.exists.assert_called_once_with("memes/meme_1.png")
        self.generator.get_file_url.assert_called_once_with("memes/meme_1.png")
        self.assertEqual(result, "http://example.com/meme_1.png")

    @patch('app.services.image_generator.funny_phrases_meme_image.default_storage')
    @patch.object(FunnyPhrasesMemeImageGenerator, 'generate_image')
    def test_get_image_new(self, mock_generate_image, mock_storage):
        mock_storage.exists.return_value = False
        mock_generate_image.return_value = ("http://example.com/new_meme_1.png", "path/to/new_meme_1.png")

        result = self.generator.get_image(self.mock_funny_template_phrases)

        mock_storage.exists.assert_called_once_with("memes/meme_1.png")
        mock_generate_image.assert_called_once_with(self.mock_funny_template_phrases)
        self.assertEqual(result, "http://example.com/new_meme_1.png")

    @patch.object(FunnyPhrasesMemeImageGenerator, 'get_image_from_url')
    @patch.object(FunnyPhrasesMemeImageGenerator, '_draw_phrases')
    @patch.object(FunnyPhrasesMemeImageGenerator, 'save_image')
    @patch.object(FunnyPhrasesMemeImageGenerator, 'get_file_url')
    def test_generate_image(self, mock_get_file_url, mock_save_image, mock_draw_phrases, mock_get_image_from_url):
        mock_img = Image.new('RGB', (1000, 1000))
        mock_get_image_from_url.return_value = mock_img
        mock_save_image.return_value = "path/to/meme_1.png"
        mock_get_file_url.return_value = "http://example.com/meme_1.png"

        result = self.generator.generate_image(self.mock_funny_template_phrases)

        mock_get_image_from_url.assert_called_once_with("http://example.com/image.jpg")
        mock_draw_phrases.assert_called_once()
        mock_save_image.assert_called_once_with(mock_img, "meme_1")
        mock_get_file_url.assert_called_once_with("path/to/meme_1.png")
        self.assertEqual(result, ("http://example.com/meme_1.png", "path/to/meme_1.png"))

    @patch.object(FunnyPhrasesMemeImageGenerator, 'draw_text')
    def test_draw_phrases(self, mock_draw_text):
        mock_draw = MagicMock(spec=ImageDraw.ImageDraw)
        mock_img = MagicMock(spec=Image.Image)
        mock_font = MagicMock(spec=ImageFont.ImageFont)
        config = ImageConfig()

        self.generator._draw_phrases(mock_draw, mock_img, self.mock_funny_template_phrases, mock_font, config)

        mock_draw_text.assert_any_call(mock_draw, mock_img, "Top Text", "top", mock_font, config)
        mock_draw_text.assert_any_call(mock_draw, mock_img, "Bottom Text", "bottom", mock_font, config)
        self.assertEqual(mock_draw_text.call_count, 2)
