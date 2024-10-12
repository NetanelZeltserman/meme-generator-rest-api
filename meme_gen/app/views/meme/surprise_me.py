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

            serializer = self.get_serializer(surprise_phrase)
            return Response(serializer.data)

        except Exception as e:
            return ExceptionsFactory.handle(e)