from rest_framework import serializers
from .models import Requests, Profile


class RequestsSerializer(serializers.ModelSerializer):

    class Meta:

        model = Requests
        fields = ('id', 'description', 'type', 'date_created', 'date_appointment', 'date_completed',
                  'accepter_rated_positive', 'requester_rated_positive', 'reported')
        http_method_names = ['GET']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile
        fields = ('id', 'created_count', 'accepted_count', 'deleted_count', 'canceled_count', 'completed_count', 'other_user_messaged_count',
                  'positive_feedback_count', 'negative_feedback_count', 'reported_count', 'is_organization', 'user_anniversary')
        http_method_names = ['GET']

