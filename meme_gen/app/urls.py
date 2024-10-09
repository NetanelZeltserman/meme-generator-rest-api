from django.urls import path
from app.views.hello_world import HelloWorldView


urlpatterns = [
    path('hello_world/', HelloWorldView.as_view(), name='hello_world'),
]