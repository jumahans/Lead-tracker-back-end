from django.contrib.auth.models import User 
from rest_framework import serializers
from .models import Freelancer, Lead, CallStatus


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class Freelance(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ['id', 'skills', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        # Get the user from the request context
        user = self.context['request'].user
        validated_data['user'] = user
        details = Freelancer.objects.create(**validated_data)
        return details


# serializers.py
# serializers.py
class Leads(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'name', 'phone', 'email', 'rating', 'website', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # Extract freelancer from context, do NOT include it in validated_data
        freelancer = self.context.get('freelancer')
        if not freelancer:
            raise serializers.ValidationError("Freelancer must be provided")

        # Handle missing email gracefully
        if 'email' in validated_data and (not validated_data['email'] or validated_data['email'] == 'N/A'):
            validated_data['email'] = None

        # Handle missing phone gracefully
        if 'phone' in validated_data and (not validated_data['phone'] or validated_data['phone'] == 'N/A'):
            validated_data['phone'] = None

        # Handle missing website gracefully
        if 'website' in validated_data and (not validated_data['website'] or validated_data['website'] == 'No Website'):
            validated_data['website'] = None

        # Pass freelancer separately
        lead = Lead.objects.create(freelancer=freelancer, **validated_data)
        return lead





class CallStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallStatus
        fields = ['called']
    



