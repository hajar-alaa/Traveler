from rest_framework import serializers
from .models import UserProfile, Post, Message, Location, Activity, WorkPlace, Visit 
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        depth = 1


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Post
        fields = '__all__'
        depth = 1


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(required=True)

    class Meta:
        model = Message
        fields = '__all__'
        depth = 1


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Location
        fields = '__all__'
        depth = 1


class WorkPlaceSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = WorkPlace
        fields = '__all__'        



class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'                