from django.urls import include, path
from rest_framework import routers
from account_management import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('create_user/', views.create_user),
    path('login/', views.login),
    path('logout/', views.logout),
    path('friends/add/', views.add_friend),
    path('friends/fetch/', views.fetch_friends),
    path('friends/requests/fetch/', views.fetch_friend_requests),
    path('friends/requests/accept/', views.accept_friend_request),
    path('friends/requests/decline/', views.decline_friend_request),
]