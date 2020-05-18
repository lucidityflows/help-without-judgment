from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.utils import timezone
from PIL import Image


# REQUEST_TYPES = types of volunteering requests that the user will be able to choose. Every requests must be associated
#                 with one of these types.
REQUEST_TYPES = [
    ('Furniture Service', 'Furniture Service'),
    ('Interpreter Service', 'Interpreter Service'),
    ('Transportation Service', 'Transportation Service'),
    ('Clothing Service', 'Clothing Service'),
    ('Food Service', 'Food Service'),
]

# FEEDBACK_TYPES = types of feedback that can be left at the conclusion of a service request. 'None' is the default
#                  value until feedback has been left at the completion of a service requests.
FEEDBACK_TYPES = [
    ('None', 'None'),
    ('Positive', 'Positive'),
    ('Negative', 'Negative'),
]

# SUPPORT_TICKET_STATUS = indicates the status of a Support Ticket. 'Pending' is the default status, until an moderator
#                         or admin addresses to Support Ticket.
SUPPORT_TICKET_STATUS = [
    ('p', 'Pending'),
    ('i', 'In-Progress'),
    ('c', 'Closed'),
]

# Model Name: Requests
# Description: The Requests model represents a volunteer request which is created by a User who is the Requester and
#              fulfilled by a different User who is the Accepter. As the Request goes through its lifecycle (created,
#              , accepted, pending appointment, completed), it is updated to reflect its current status. When it is
#              completed, and the other user is rated by feedback, it should not undergo any other updates. Completed
#              Request information is viewable to the Accepter and Requester.


class Requests(models.Model):

    status = models.CharField(max_length=50, default="Incomplete")
    description = models.CharField(max_length=500)
    type = models.CharField(choices=REQUEST_TYPES, max_length=50, default='Item Service')
    date_created = models.DateTimeField(auto_now_add=True)
    date_appointment = models.DateTimeField(null=True)
    date_completed = models.DateTimeField(null=True)
    appointment_confirmed = models.BooleanField(default=False)
    appointment_suggested = models.BooleanField(default=False)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    accepter = models.CharField(max_length=150, null=True)
    accepter_is_verified = models.BooleanField(default=False)
    accepter_rated_positive = models.BooleanField(null=True)
    requester_rated_positive = models.BooleanField(null=True)
    reported = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class RequestForm(ModelForm):

    class Meta:
        model = Requests
        fields = ['type', 'description']
        widgets = {'description': forms.Textarea}
        #description = forms.CharField(widget=forms.Textarea)


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

# Model Name: SupportTicket
# Description: The SupportTicket model represents a User generated request for moderator or admin user to assist with
#              an issue the User is experiencing.


class SupportTicket(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500)
    body = models.CharField(max_length=500)
    date_created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=SUPPORT_TICKET_STATUS, default='p')
    support_comment = models.CharField(max_length=200, default="Your issue is being processed. Check for updates later.")

    def __str__(self):

        return f'Subject: {self.subject}'


class SupportTicketForm(ModelForm):

    class Meta:
        model = SupportTicket
        fields = ['subject', 'body']
        widgets = {'body': forms.Textarea}

# Model Name: Profile
# Description: The Profile model represents a User Profile. It stores information about a User's profile image,
#              whether or not they have moderator status, if they are an individual or organization, and the historical
#              counts on their user stats. This information will be used to create graphs for the user to view, and
#              to export in the public API.


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default_profile_image.jpg", upload_to="profile_pics")
    created_count = models.IntegerField(default=0)
    accepted_count = models.IntegerField(default=0)
    deleted_count = models.IntegerField(default=0)
    completed_count = models.IntegerField(default=0)
    canceled_count = models.IntegerField(default=0)
    other_user_messaged_count = models.IntegerField(default=0)
    reported_count = models.IntegerField(default=0)
    positive_feedback_count = models.IntegerField(default=0)
    negative_feedback_count = models.IntegerField(default=0)
    user_anniversary = models.DateField(auto_now_add=True)
    is_moderator = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)
        image = Image.open(self.image.path)

        if image.height > 500 or image.width > 500:

            output_size = (500, 500)
            image.thumbnail(output_size)
            image.save(self.image.path)

