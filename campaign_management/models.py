import uuid

from django.db import models


class Campaign(models.Model):
    campaign_id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4)
    active_scene_id = models.UUIDField(null=True)
    dm = models.UUIDField(unique=False)
    campaign_name = models.CharField(max_length=64, unique=False)
    campaign_description = models.CharField(max_length=500, unique=False, null=True)


class Scene(models.Model):
    campaign_id = models.UUIDField(primary_key=False, unique=False)
    scene_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    scene_name = models.CharField(max_length=64)


class SceneAssetData(models.Model):
    scene_id = models.UUIDField(unique=False, default=uuid.uuid4)
    asset_id = models.CharField(max_length=256, unique=False)
    asset_x_pos = models.FloatField(null=True)
    asset_y_pos = models.FloatField(null=True)
    asset_z_pos = models.FloatField(null=True)
    asset_x_rot = models.FloatField(null=True)
    asset_y_rot = models.FloatField(null=True)
    asset_z_rot = models.FloatField(null=True)
    asset_x_scale = models.FloatField(null=True)
    asset_y_scale = models.FloatField(null=True)
    asset_z_scale = models.FloatField(null=True)


class SceneCharacterData(models.Model):
    campaign_id = models.UUIDField(unique=False)
    scene_id = models.UUIDField(unique=False)
    character_id = models.UUIDField(unique=False, null=True)
    character_x_pos = models.FloatField(null=True)
    character_y_pos = models.FloatField(null=True)
    character_z_pos = models.FloatField(null=True)
    character_x_rot = models.FloatField(null=True)
    character_y_rot = models.FloatField(null=True)
    character_z_rot = models.FloatField(null=True)
    character_x_scale = models.FloatField(null=True)
    character_y_scale = models.FloatField(null=True)
    character_z_scale = models.FloatField(null=True)


class CampaignMembers(models.Model):
    campaign_id = models.UUIDField(unique=False)
    player_id = models.UUIDField(unique=False)


class Character(models.Model):
    character_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    klass = models.CharField(max_length=32, unique=False)
    level = models.IntegerField(default=1)
    background = models.CharField(max_length=64, unique=False)
    playerName = models.CharField(max_length= 64, unique=False)
    race = models.CharField(max_length=32, unique=False)
    alignment = models.CharField(max_length=64, unique=False, default='Neutral')
    XP = models.IntegerField(default=0)
    armorClass = models.IntegerField()
    initiative = models.IntegerField()
    speed = models.IntegerField(default=30)
    inspiration = models.BooleanField(default=False)
    proficiencyBonus = models.IntegerField()
    strengthMod = models.IntegerField()
    dexMod = models.IntegerField()
    conMod = models.IntegerField()
    intelligenceMod = models.IntegerField()
    wisdomMod = models.IntegerField()
    charismaMod = models.IntegerField()
    strength = models.IntegerField()
    dex = models.IntegerField()
    con = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()
    strengthSave = models.IntegerField()
    dexSave = models.IntegerField()
    conSave = models.IntegerField()
    intelligenceSave = models.IntegerField()
    wisdomSave = models.IntegerField()
    charismaSave = models.IntegerField()
    acrobatics = models.IntegerField()
    animalHandling = models.IntegerField()
    arcana = models.IntegerField()
    athletics = models.IntegerField()
    deception = models.IntegerField()
    history = models.IntegerField()
    insight = models.IntegerField()
    intimidation = models.IntegerField()
    investigation = models.IntegerField()
    medicine = models.IntegerField()
    nature = models.IntegerField()
    perception = models.IntegerField()
    performance = models.IntegerField()
    persuasion = models.IntegerField()
    religion = models.IntegerField()
    sleightOfHand = models.IntegerField()
    stealth = models.IntegerField()
    survival = models.IntegerField()
    maxHP = models.IntegerField()
    currentHP = models.IntegerField()
    totalHitDice = models.IntegerField()
    currentHitDice = models.IntegerField()
