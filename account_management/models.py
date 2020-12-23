import uuid
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    player_id = models.UUIDField(unique=True, null=False, primary_key=True, default=uuid.uuid4)
    hours_played = models.IntegerField(null=True, default=0)

    class Meta:
        db_table = 'player'


class Friendships(models.Model):
    friend_1 = models.UUIDField(unique=False)
    friend_2 = models.UUIDField(unique=False)
    date_added = models.DateTimeField(null=False, default=datetime.now, editable=False)

    class Meta:
        db_table = 'friendships'


class FriendRequest(models.Model):
    requester = models.UUIDField(unique=False)
    addressee = models.UUIDField(unique=False)
    status = models.CharField(max_length=1, unique=False, default='R', null=False)
    date_requested = models.DateTimeField(null=False, default=datetime.now)
    date_updated = models.DateTimeField(null=False, default=datetime.now, editable=False)

    class Meta:
        db_table = 'friend_requests'
