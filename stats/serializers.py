from rest_framework import serializers
from django.contrib.auth.models import User

from django.forms import ModelForm
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'gender', 'birth_date']

    

class ExcerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"
