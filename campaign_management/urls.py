from django.urls import path
from campaign_management import views

urlpatterns = [
    path('new/', views.create_campaign),
    path('fetch/', views.fetch_campaigns)
]