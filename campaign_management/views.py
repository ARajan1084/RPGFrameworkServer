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
from campaign_management.models import Campaign, CampaignMembers, SceneAssetData, Scene


@api_view(['POST'])
def create_campaign(request):
    json_data = json.loads(str(request.body, encoding='UTF-8'))
    try:
        player_id = json_data['playerID']
        campaign_name = json_data['campaignName']
        campaign = Campaign(dm=player_id, campaign_name=campaign_name)
        campaign.save()
        scene = Scene(campaign_id=campaign.campaign_id, scene_name='Default')
        scene.save()
        ground = SceneAssetData(scene_id=scene.scene_id, asset_id="Ground",
                                asset_x_pos=0, asset_y_pos=0, asset_z_pos=0, asset_x_rot=0, asset_y_rot=0, asset_z_rot=0,
                                asset_x_scale=5, asset_y_scale=5, asset_z_scale=5)
        ground.save()
        campaign.active_scene_id = scene.scene_id
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
                                           'campaign_id': str(campaign.campaign_id.hex),
                                           'campaign_description': campaign.campaign_description,
                                           'dm_name': player_name})
        for campaign_id in CampaignMembers.objects.filter(player_id=player_id):
            campaign = Campaign.objects.get(campaign_id=campaign_id)
            dm = Player.objects.get(player_id=campaign.dm)
            campaigns.get('Items').append({'campaign_name': campaign.campaign_name,
                                           'campaign_id': str(campaign.campaign_id.hex),
                                           'campaign_description': campaign.campaign_description,
                                           'dm_name': dm.user.first_name + ' ' + dm.user.last_name})
        return Response(data=json.dumps(campaigns), status=status.HTTP_200_OK, content_type='application/json')
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fetch_active_scene(request):
    json_data = json.loads(str(request.body, encoding='UTF-8'))
    try:
        campaign_id = json_data['campaignID']
        active_scene_id = Campaign.objects.get(campaign_id=campaign_id).active_scene_id
        data = {'campaign_id': campaign_id,
                'scene_id': str(active_scene_id.hex)}
        return Response(data=json.dumps(data), status=status.HTTP_200_OK, content_type='application/json')
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def fetch_scene_asset_data(request):
    json_data = json.loads(str(request.body, encoding='UTF-8'))
    try:
        scene_id = json_data['scene_id']
        assets = {'Items': []}
        for asset in SceneAssetData.objects.filter(scene_id=scene_id):
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


@api_view(['POST'])
def save_scene_asset_data(request, scene_id):
    json_data = json.loads(str(request.body, encoding='UTF-8'))
    try:
        assets = json_data['Items']
        clear_scene_asset_data(scene_id)
        for asset in assets:
            asset_data = SceneAssetData(scene_id=scene_id,
                                       asset_id=asset['asset_id'],
                                       asset_x_pos=asset['x_pos'],
                                       asset_y_pos=asset['y_pos'],
                                       asset_z_pos=asset['z_pos'],
                                       asset_x_rot=asset['x_rot'],
                                       asset_y_rot=asset['y_rot'],
                                       asset_z_rot=asset['z_rot'],
                                       asset_x_scale=asset['x_scale'],
                                       asset_y_scale=asset['y_scale'],
                                       asset_z_scale=asset['z_scale'])
            asset_data.save()
        return Response(status=status.HTTP_200_OK)
    except:
        traceback.print_exc()
        return Response(status=status.HTTP_400_BAD_REQUEST)


def clear_scene_asset_data(scene_id):
    asset_data = SceneAssetData.objects.filter(scene_id=scene_id)
    for asset in asset_data:
        asset.delete()
    ground = SceneAssetData(scene_id=scene_id, asset_id="Ground",
                            asset_x_pos=0, asset_y_pos=0, asset_z_pos=0, asset_x_rot=0, asset_y_rot=0, asset_z_rot=0,
                            asset_x_scale=5, asset_y_scale=5, asset_z_scale=5)
    ground.save()
