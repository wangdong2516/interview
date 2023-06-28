from django.contrib.auth import login, authenticate
from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from user.serializer import UserLoginSerializer
from utils.exception import InterviewAPIException


# Create your views here.
from rest_framework.generics import DestroyAPIView


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cleaned_data = serializer.data
            user = authenticate(
                username=cleaned_data["username"], password=cleaned_data["password"]
            )
            if not user:
                raise InterviewAPIException.CUSTOMER_INFO_NOT_EXISIS
            user_info = UserLoginSerializer(user).data
            user_info.pop("password", None)
            return Response(data={"user_info": user_info})
