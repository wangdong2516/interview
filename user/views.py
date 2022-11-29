from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class UserLoginView(APIView):

    def get(self, request):
        return Response({"message": 'hello'})
