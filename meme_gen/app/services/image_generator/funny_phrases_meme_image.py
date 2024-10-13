from app.services.image_generator.base import BaseImageGenerator, ImageConfig
from django.core.files.storage import default_storage
from app.models import FunnyTemplatePhrases
from PIL import ImageDraw, ImageFont, Image

class FunnyPhrasesMemeImageGenerator(BaseImageGenerator):
    def get_image(self, funny_template_phrases: FunnyTemplatePhrases) -> str:
        image_filename = f"memes/meme_{funny_template_phrases.id}.png"

        if default_storage.exists(image_filename):
            return self.get_file_url(image_filename)

        return self.generate_image(funny_template_phrases)[0]

    def generate_image(self, funny_template_phrases: FunnyTemplatePhrases, config: ImageConfig = ImageConfig()) -> tuple[str, str]:
        img = self.get_image_from_url(funny_template_phrases.template.image_url)
        draw = ImageDraw.Draw(img)

        font_size = int(img.width / config.font_size_ratio)
        font = ImageFont.load_default().font_variant(size=font_size)

        self._draw_phrases(draw, img, funny_template_phrases, font, config)

        file_path = self.save_image(img, f"meme_{funny_template_phrases.id}")
        file_url = self.get_file_url(file_path)

        return file_url, file_path

    def _draw_phrases(self, draw: ImageDraw.ImageDraw, img: Image.Image, funny_template_phrases: FunnyTemplatePhrases, font: ImageFont.ImageFont, config: ImageConfig):
        phrases = [
            ('top', funny_template_phrases.top_phrase),
            ('bottom', funny_template_phrases.bottom_phrase)
        ]

        for position, text in phrases:
            self.draw_text(draw, img, text, position, font, config)
