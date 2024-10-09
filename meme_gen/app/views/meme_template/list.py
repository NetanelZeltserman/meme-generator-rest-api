from app.serializers.meme_template import MemeTemplateSerializer
from rest_framework import generics, mixins
from app.models import MemeTemplate

class MemeTemplateList(mixins.ListModelMixin,
                       generics.GenericAPIView):
    queryset = MemeTemplate.objects.all()
    serializer_class = MemeTemplateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
