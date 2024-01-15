from django.urls import path , include
from app.consumers import ChatConsumer
 
# Here, "" is routing to the URL ChatConsumer which 
# will handle the chat functionality.
websocket_urlpatterns = [
    path("homechat/" , ChatConsumer.as_asgi()) , 
]