from app.serializers.meme_rating import MemeRatingSerializer
from rest_framework.permissions import IsAuthenticated
from app.exceptions.factory import ExceptionsFactory
from rest_framework.response import Response
from rest_framework import generics, status
from app.models import Meme

class MemeRateView(generics.CreateAPIView):
    queryset = Meme.objects.all()
    serializer_class = MemeRatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return ExceptionsFactory.handle(e)