import json
import traceback
from itertools import chain

from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from account_management.models import Player
from campaign_management.models import Campaign, CampaignMembers, SceneAssetData


@api_view(['POST'])
def create_campaign(request):
    json_data = json.loads(str(request.body, encoding='UTF-8'))
    try:
        player_id = json_data['playerID']
        campaign_name = json_data['campaignName']
        campaign = Campaign(dm=player_id, campaign_name=campaign_name)
        campaign.save()
        return Response(status=status.HTTP_201_CREATED)
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fetch_campaigns(request):
    json_data = json.loads(str(request.body, encoding='UTF-8'))
    try:
        player_id = json_data['playerID']
        campaigns = {'Items': []}
        player = Player.objects.get(player_id=player_id)
        player_name = player.user.first_name + ' ' + player.user.last_name
        for campaign in Campaign.objects.filter(dm=player_id):
            campaigns.get('Items').append({'campaign_name': campaign.campaign_name,
                                           'campaign_description': campaign.campaign_description,
                                           'dm_name': player_name})
        for campaign_id in CampaignMembers.objects.filter(player_id=player_id):
            campaign = Campaign.objects.get(campaign_id=campaign_id)
            dm = Player.objects.get(player_id=campaign.dm)
            campaigns.get('Items').append({'campaign_name': campaign.campaign_name,
                                           'campaign_description': campaign.campaign_description,
                                           'dm_name': dm.user.first_name + ' ' + dm.user.last_name})
        return Response(data=json.dumps(campaigns), status=status.HTTP_200_OK, content_type='application/json')
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fetch_scene_asset_data(request):
    json_data = json.loads(str(request.body, encoding='UTF-8'))
    try:
        scene_id = json_data['scene_id']
        campaign_id = json_data['campaign_id']
        assets = {'Items': []}
        for asset in SceneAssetData.objects.filter(scene_id=scene_id, campaign_id=campaign_id):
            assets.get('Items').append({'asset_id': asset.asset_id,
                                        'x_pos': asset.asset_x_pos,
                                        'y_pos': asset.asset_y_pos,
                                        'z_pos': asset.asset_z_pos,
                                        'x_rot': asset.asset_x_rot,
                                        'y_rot': asset.asset_y_rot,
                                        'z_rot': asset.asset_z_rot,
                                        'x_scale': asset.asset_x_scale,
                                        'y_scale': asset.asset_y_scale,
                                        'z_scale': asset.asset_z_scale})
        return Response(data=json.dumps(assets), status=status.HTTP_200_OK, content_type='application/json')
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)