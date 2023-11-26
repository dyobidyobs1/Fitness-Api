from rest_framework import serializers
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import *


class StatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stats
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['weight', 'height', 'image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'gender', 'birth_date', 'weight', 'height', 'image',]

class ExcerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"



class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"

class LeaderUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'image']

class LeaderboardsSerializer(serializers.ModelSerializer):
    user = LeaderUserSerializer()
    
    class Meta:
        model = Stats
        fields = (
            'user',
            'current_level',
        )

class GenerarePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratePlan
        fields = "__all__"