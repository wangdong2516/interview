from django.urls import path
from user.views import UserLoginView


urlpatterns = [
    path('login/', UserLoginView.as_view()),
]
