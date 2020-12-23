import traceback

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import exception_handler

from account_management.models import Player, FriendRequest
from account_management.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
def create_user(request):
    json_data = json.loads(str(request.body, encoding='UTF-8'))
    try:
        user = User.objects.create_user(
            email=json_data['email'],
            username=json_data['username'],
            password=json_data['password'],
            first_name=json_data['first_name'],
            last_name=json_data['last_name'],
        )
        user.save()
        player = Player.objects.create(user=user)
        player.save()
        return Response(json_data, status=status.HTTP_201_CREATED)
    except:
        traceback.print_exc()
        response = Response(data='USERNAME TAKEN', status=status.HTTP_400_BAD_REQUEST)
        return response


@api_view(['POST'])
def login(request):
    json_data = json.loads(str(request.body, encoding='UTF-8'))
    try:
        username = json_data['username']
        password = json_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        player = Player.objects.get(user=user)
        return Response(data=player.player_id, status=status.HTTP_202_ACCEPTED)
    except:
        traceback.print_exc()
        response = Response(status=status.HTTP_400_BAD_REQUEST)
        return response


@api_view(['POST'])
def logout(request):
    try:
        auth_logout(request)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_friend(request):
    try:
        json_data = json.loads(str(request.body, encoding='UTF-8'))
        player_id = json_data['player_id']
        friend_username = json_data['friend_username']
        friend_id = Player.objects.get(user=User.objects.get(username=friend_username)).player_id
        friend_request = FriendRequest(requester=player_id, addressee=friend_id)
        friend_request.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)