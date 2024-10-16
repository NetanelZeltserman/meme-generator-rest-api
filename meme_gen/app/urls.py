from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from app.views.meme.surprise_me import MemeSurpriseMeView
from app.views.meme.list_and_create import MemeListCreateView
from app.views.meme.random import MemeRandomView
from app.views.meme_template.list import MemeTemplateListView
from app.views.meme.retrieve import MemeRetrieveView
from app.views.meme.rate import MemeRateView
from app.views.meme.top_ten_rated import MemeTopTenRatedView
from django.urls import path


urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('login/', TokenObtainPairView.as_view(), name='token_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('templates/', MemeTemplateListView.as_view(), name='meme_template_list'),
    path('memes/', MemeListCreateView.as_view(), name='meme_list_create'),
    path('memes/<int:pk>/', MemeRetrieveView.as_view(), name='meme_retrieve'),

    path('memes/rate/', MemeRateView.as_view(), name='meme_rate'),
    path('memes/random/', MemeRandomView.as_view(), name='meme_random'),
    path('memes/top/', MemeTopTenRatedView.as_view(), name='meme_top_ten_rated'),

    # Bonus
    path('memes/surprise-me/', MemeSurpriseMeView.as_view(), name='meme_surprise_me'),
    path('memes/surprise-me/<int:template_id>/', MemeSurpriseMeView.as_view(), name='meme_surprise_me_with_template'),
]