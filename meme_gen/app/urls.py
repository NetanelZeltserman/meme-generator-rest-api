from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from app.views.meme_template.list import MemeTemplateList

from django.urls import path

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('templates/', MemeTemplateList.as_view(), name='meme_template_list'),
]