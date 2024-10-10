from app.serializers.meme import MemeSerializer, MemeCreateSerializer
from rest_framework.pagination import PageNumberPagination
from app.exceptions.factory import ExceptionsFactory
from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from app.models import Meme

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class MemeListCreateView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView):
    queryset = Meme.objects.all()
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return MemeCreateSerializer if self.request.method == 'POST' else MemeSerializer

    def get(self, request, *args, **kwargs):
        try:
            return self.list(request, *args, **kwargs)
        except Exception as e:
            return ExceptionsFactory.handle(e)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            meme = serializer.save()

            return Response(MemeSerializer(meme).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return ExceptionsFactory.handle(e)
