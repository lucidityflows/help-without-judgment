from django.contrib import admin
from .models import Requests, Profile, SupportTicket

# Register your models here.
admin.site.register(Requests)
admin.site.register(Profile)
admin.site.register(SupportTicket)


admin.site.site_header = "Help Without Judgment - Admin Dashboard"
