from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.utils import timezone

# Create your models here.


REQUEST_TYPES = [
    ('Furniture Service', 'Furniture Service'),
    ('Interpreter Service', 'Interpreter Service'),
    ('Transportation Service', 'Transportation Service'),
    ('Clothing Service', 'Clothing Service'),
    ('Food Service', 'Food Service'),
]

FEEDBACK_TYPES = [
    ('None', 'None'),
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
]


class Requests(models.Model):

    status = models.CharField(max_length=50, default="Incomplete")
    description = models.CharField(max_length=250)
    type = models.CharField(choices=REQUEST_TYPES, max_length=50, default='Item Service')
    date_created = models.DateTimeField(auto_now_add=True)
    date_appointment = models.DateTimeField(null=True)
    date_completed = models.DateTimeField(null=True)
    appointment_confirmed = models.BooleanField(default=False)
    appointment_suggested = models.BooleanField(default=False)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    accepter = models.CharField(max_length=150, null=True)
    accepter_feedback = models.CharField(max_length=250, default='None')
    requester_feedback = models.CharField(max_length=250, default='None')

    def __str__(self):
        return self.description


class RequestForm(ModelForm):

    class Meta:
        model = Requests
        fields = ['description', 'type']


class AcceptRequestForm(ModelForm):

    class Meta:
        model = Requests
        fields = ['accepter']


class CancelRequestForm(ModelForm):

    class Meta:
        model = Requests
        fields = ['accepter']


class DeleteRequestForm(ModelForm):

    class Meta:
        model = Requests
        fields = ['requester']


class CloseRequestForm(ModelForm):

    class Meta:
        model = Requests
        fields = ['status']


class ScheduleAppointmentForm(forms.Form):

    class Meta:
        model = Requests
        fields = ['date_appointment']
        widgets = {
            'date_appointment': forms.DateTimeInput(attrs={'class': 'datetime-input', 'format': '%Y-%m-%d %H:%M'})
        }


class ConfirmAppointmentForm(ModelForm):

    class Meta:
        model = Requests
        fields = ['appointment_confirmed']


class DateForm(forms.Form):

    date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M', ''], required=False)

