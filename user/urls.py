from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    #path('/dashboard', views.dashboard, name='dashboard'),
    path('open_requests', views.open_requests, name='open_requests'),
    path('create_request', views.create_request, name='create_request'),
]