from django.urls import path
from campaign_management import views

urlpatterns = [
    path('new/', views.create_campaign),
    path('fetch/', views.fetch_campaigns),
    path('scenes/fetch', views.fetch_active_scene),
    path('scenes/assets/fetch', views.fetch_scene_asset_data)
]