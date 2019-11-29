from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('open_requests', views.open_requests, name='open_requests'),
    path('create_request', views.create_request, name='create_request'),
    path('view_past_requests', views.past_requests, name='past_requests'),
    path('profile', views.profile, name='profile'),
    path('inbox', views.inbox, name='inbox'),
]
