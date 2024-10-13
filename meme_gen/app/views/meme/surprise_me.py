from app.services.image_generator.funny_phrases_meme_image import FunnyPhrasesMemeImageGenerator
from app.repositories.funny_template_phrases_repository import FunnyTemplatePhrasesRepository
from app.serializers.funny_template_phrases import FunnyTemplatePhrasesSerializer
from rest_framework.permissions import IsAuthenticated
from app.exceptions.factory import ExceptionsFactory
from rest_framework.response import Response
from rest_framework import generics

class MemeSurpriseMeView(generics.RetrieveAPIView):
    serializer_class = FunnyTemplatePhrasesSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, template_id=None):
        try:
            surprise_phrase = FunnyTemplatePhrasesRepository.get_random_funny_template_phrase(template_id)
            img_url = FunnyPhrasesMemeImageGenerator().get_image(surprise_phrase)

            response_data = self.get_serializer(surprise_phrase).data
            response_data['image_url'] = img_url

            return Response(response_data)

        except Exception as e:
            return ExceptionsFactory.handle(e)