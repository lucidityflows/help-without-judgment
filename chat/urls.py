from django.urls import path, re_path
from .views import ThreadView
from . import views

app_name = 'chat'

urlpatterns = [
    re_path(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view()),
]
