from rest_framework import serializers
from .models import Requests, Profile


class RequestsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Requests
        fields = ('id', 'description', 'type', 'date_created', 'date_appointment', 'date_completed',
                  'appointment_confirmed', 'appointment_suggested', 'reported')
        http_method_names = ['GET']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile
        fields = ('id', 'created_count', 'accepted_count', 'deleted_count', 'reported_count', 'user_anniversary')
        http_method_names = ['GET']

