from app.repositories.meme_repository import MemeRepository
from rest_framework.permissions import IsAuthenticated
from app.exceptions.factory import ExceptionsFactory
from app.serializers.meme import MemeSerializer
from rest_framework.response import Response
from rest_framework import generics

class MemeRandomView(generics.RetrieveAPIView):
    serializer_class = MemeSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        try:
            random_meme = MemeRepository.get_random_meme()

            serializer = self.get_serializer(random_meme)
            return Response(serializer.data)
        
        except Exception as e:
            return ExceptionsFactory.handle(e)