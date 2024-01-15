from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from channels.auth import AuthMiddlewareStack
import os
from django.core.asgi import get_asgi_application
from django.urls import path
from app.consumers import ChatConsumer 
from app import routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
	{
		"http" : get_asgi_application() , 
		"websocket" : AuthMiddlewareStack(
			URLRouter(
				routing.websocket_urlpatterns
			) 
		)
	}
)


