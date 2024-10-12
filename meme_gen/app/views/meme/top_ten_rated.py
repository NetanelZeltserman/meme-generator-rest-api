from app.repositories.meme_repository import MemeRepository
from rest_framework.permissions import IsAuthenticated
from app.exceptions.factory import ExceptionsFactory
from app.serializers.meme import MemeSerializer
from rest_framework.response import Response
from rest_framework import generics

class MemeTopTenRatedView(generics.ListAPIView):
    serializer_class = MemeSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            top_memes = MemeRepository.get_top_rated_memes(limit=10)

            serializer = self.get_serializer(top_memes, many=True)
            return Response(serializer.data)

        except Exception as e:
            return ExceptionsFactory.handle(e)