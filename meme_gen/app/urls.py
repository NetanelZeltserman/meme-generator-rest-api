from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from app.views.meme.list_and_create import MemeListCreateView
from app.views.meme.random import MemeRandomView
from app.views.meme_template.list import MemeTemplateList
from app.views.meme.retrieve import MemeRetrieve
from app.views.meme.rate import MemeRateView
from django.urls import path


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('templates/', MemeTemplateList.as_view(), name='meme_template_list'),
    path('memes/', MemeListCreateView.as_view(), name='meme_list_create'),
    path('memes/<int:pk>/', MemeRetrieve.as_view(), name='meme_retrieve'),

    path('memes/rate/', MemeRateView.as_view(), name='meme_rate'),
    path('memes/random/', MemeRandomView.as_view(), name='meme_random'),
]