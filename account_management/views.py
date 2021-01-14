import traceback
import uuid
from itertools import chain

from django.utils import timezone
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

from account_management.models import Player, FriendRequest, Friendship
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
        player_info = {'playerID': str(player.player_id.hex),
                       'username': str(player.user.username),
                       'firstName': player.user.first_name,
                       'lastName': player.user.last_name}
        print(player_info)
        return Response(data=json.dumps(player_info), status=status.HTTP_202_ACCEPTED, content_type='application/json')
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
def fetch_friends(request):
    try:
        json_data = json.loads(str(request.body, encoding='UTF-8'))
        player_id = json_data['playerID']
        friendships = {'Items': []}
        for friendship in Friendship.objects.filter(friend_1=player_id):
            friend = Player.objects.get(player_id=friendship.friend_2)
            friendships.get('Items').append({'player_id': str(friend.player_id.hex),
                                             'username': friend.user.username,
                                             'firstName': friend.user.first_name,
                                             'lastName': friend.user.last_name})
        for friendship in Friendship.objects.filter(friend_2=player_id):
            friend = Player.objects.get(player_id=friendship.friend_1)
            friendships.get('Items').append({'player_id': str(friend.player_id.hex),
                                             'username': friend.user.username,
                                             'firstName': friend.user.first_name,
                                             'lastName': friend.user.last_name})
        return Response(data=json.dumps(friendships), status=status.HTTP_200_OK, content_type='application/json')
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fetch_friend_requests(request):
    try:
        json_data = json.loads(str(request.body, encoding='UTF-8'))
        player_id = json_data['playerID']
        friend_requests = {'Items': []}
        for friend_request in FriendRequest.objects.filter(addressee=player_id, status='R'):
            requester = Player.objects.get(player_id=friend_request.requester)
            friend_requests.get('Items').append({
                'username': requester.user.username,
                'firstName': requester.user.first_name,
                'lastName': requester.user.last_name
            })
        return Response(data=json.dumps(friend_requests), status=status.HTTP_200_OK, content_type='application/json')
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_friend(request):
    try:
        json_data = json.loads(str(request.body, encoding='UTF-8'))
        player_id = uuid.UUID(json_data['player_id'])
        friend_username = json_data['friend_username']
        friend_id = Player.objects.get(user=User.objects.get(username=friend_username)).player_id
        # Check if requester and addressee are already friends
        if Friendship.objects.filter(friend_1=friend_id, friend_2=player_id).exists() or \
                Friendship.objects.filter(friend_1=player_id, friend_2=friend_id):
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        # Check if a friend request has already been sent between them
        if FriendRequest.objects.filter(requester=player_id, addressee=friend_id) or \
                FriendRequest.objects.filter(requester=friend_id, addressee=player_id):
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        # Create friend request
        friend_request = FriendRequest(requester=player_id, addressee=friend_id)
        friend_request.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def accept_friend_request(request):
    try:
        json_data = json.loads(str(request.body, encoding='UTF-8'))
        player_id = json_data['player_id']
        friend_username = json_data['friend_username']
        friend_id = Player.objects.get(user=User.objects.get(username=friend_username)).player_id
        # Check if requester and addressee are already friends
        if Friendship.objects.filter(friend_1=friend_id, friend_2=player_id).exists() or \
                Friendship.objects.filter(friend_1=player_id, friend_2=friend_id):
            return Response(status=status.HTTP_208_ALREADY_REPORTED)
        # Create and save the friendship
        new_friendship = Friendship(friend_1=player_id, friend_2=friend_id)
        new_friendship.save()
        # Updates the status of the friend request
        friend_request = FriendRequest.objects.get(requester=friend_id, addressee=player_id)
        friend_request.status = 'A'
        friend_request.date_updated = timezone.now()
        friend_request.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def decline_friend_request(request):
    try:
        json_data = json.loads(str(request.body, encoding='UTF-8'))
        player_id = json_data['player_id']
        friend_username = json_data['friend_username']
        friend_id = Player.objects.get(user=User.objects.get(username=friend_username)).player_id
        # Updates the status of the friend request
        friend_request = FriendRequest.objects.get(requester=friend_id, addressee=player_id)
        friend_request.status = 'D'
        friend_request.date_updated = timezone.now()
        friend_request.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)