from rest_framework.permissions import IsAuthenticated
from app.exceptions.factory import ExceptionsFactory
from app.serializers.meme import MemeSerializer
from rest_framework import generics, mixins
from app.models import Meme
class MemeRetrieve(mixins.RetrieveModelMixin,
                 generics.GenericAPIView):
    queryset = Meme.objects.all()
    serializer_class = MemeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except Exception as e:
            return ExceptionsFactory.handle(e)
