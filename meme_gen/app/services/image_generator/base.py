from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont
from abc import ABC, abstractmethod
from dataclasses import dataclass
from django.conf import settings
from django.db import models
from io import BytesIO
import requests

@dataclass
class ImageConfig:
    font_size_ratio: int = 20
    stroke_width: int = 2
    fill: str = "white"
    stroke_fill: str = "black"

class BaseImageGenerator(ABC):
    @abstractmethod
    def get_image(self, model: models.Model) -> str:
        pass
    
    @abstractmethod
    def generate_image(self, image_url: str, top_text: str, bottom_text: str, config: ImageConfig) -> Image.Image:
        pass

    @staticmethod
    def get_image_from_url(url: str) -> Image.Image:
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    @staticmethod
    def draw_text(draw: ImageDraw.ImageDraw, img: Image.Image, text: str, position: str, font: ImageFont.ImageFont, config: ImageConfig):
        x = img.width / 2
        y = 25 if position == 'top' else img.height - 25
        anchor = "mt" if position == 'top' else "mb"
        
        draw.text((x, y), text, font=font, fill=config.fill, stroke_width=config.stroke_width, 
                  stroke_fill=config.stroke_fill, anchor=anchor)

    @staticmethod
    def save_image(img: Image.Image, filename: str) -> str:
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)

        filename = f"{filename}.png"
        return default_storage.save(f'memes/{filename}', ContentFile(img_io.getvalue()))

    @staticmethod
    def get_file_url(file_path: str) -> str:
        return settings.BASE_URL + default_storage.url(file_path)
