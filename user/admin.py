from django.contrib import admin
from .models import Requests, Profile

# Register your models here.
admin.site.register(Requests)
admin.site.register(Profile)

admin.site.site_header = "Help Without Judgment - Admin Dashboard"
