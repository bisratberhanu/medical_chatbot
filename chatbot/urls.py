from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),        # Default route for chat UI
    path('api/chat/', views.chat_api, name='chat_api'),  # API endpoint
]