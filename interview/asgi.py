"""
ASGI config for interview project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev_settings')

# application = get_asgi_application()

# 集成django-channels功能(同时支持https协议和websocket协议)
application = ProtocolTypeRouter(
    {
        # https方式调用的asgi方法
        'http': get_asgi_application(),
        # websocket协议调用的asgi方法
        "websocket": AllowedHostsOriginValidator(
                AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
            ),
    }
)
