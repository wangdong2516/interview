from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView


# Create your views here.


class ChatIndexView(APIView):


    def get(self, request):
        return render(request, "chat/index.html")



class ChatRoomView(APIView):

    def get(self, request, room_name):
        return render(request, "chat/room.html", {"room_name": room_name})
