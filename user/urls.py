from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('requests', views.RequestsView)
router.register('profiles', views.ProfileView)

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('open_requests', views.open_requests, name='open_requests'),
    path('create_request', views.create_request, name='create_request'),
    path('view_past_requests', views.past_requests, name='past_requests'),
    path('profile', views.profile, name='profile'),
    path('inbox', views.inbox, name='inbox'),
    path('non_profits', views.non_profits, name='non_profits'),
    path('api/', include(router.urls)),
    path('support', views.support, name='support'),

]
