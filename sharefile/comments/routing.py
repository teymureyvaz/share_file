from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('<int:file_id>/',consumers.CommentConsumer),
]