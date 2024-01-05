from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import locale
import uuid

from django.core.files.storage import FileSystemStorage
from django.db import models


def create_rand_id():
        from django.utils.crypto import get_random_string
        return get_random_string(length=13, 
            allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')


class CustomUser(AbstractUser):
    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    gender = models.CharField(max_length=50, choices=GENDER, null=True, blank=True)
    birth_date = models.CharField(max_length=50, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/profile', blank=True, null=True)




class Exercise(models.Model):
    exercise_name = models.CharField(max_length=100, null=True, blank=True)
    exp_gain = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/excercise', blank=True, null=True)
    gif = models.ImageField(upload_to='uploads/excercise/gif', blank=True, null=True)


    def __str__(self):
        return f"{self.exercise_name}"

class Stats(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    available_points = models.IntegerField(default=1, null=True, blank=True)
    current_level = models.IntegerField(default=1, null=True, blank=True)
    current_exp = models.IntegerField(default=0, null=True, blank=True)
    max_exp = models.IntegerField(default=30, null=True, blank=True)
    strength = models.IntegerField(default=0, null=True, blank=True)
    endurance = models.IntegerField(default=0, null=True, blank=True)
    flexability = models.IntegerField(default=0, null=True, blank=True)
    agility = models.IntegerField(default=0, null=True, blank=True)
    available_points = models.IntegerField(default=0, null=True, blank=True)

    def level_up(self):
        print("test")
        if self.current_exp >= self.max_exp:
            excess_exp = self.max_exp - self.current_exp
            self.current_exp = excess_exp
            self.current_level = self.current_level + 1
            self.available_points += 1
            print("test")
            self.max_exp += 10
    
    def __str__(self):
        return f"{self.user} - {self.current_level}"
    
class History(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    exercise_name = models.CharField(max_length=100, null=True, blank=True)
    exercise_id = models.CharField(max_length=100, null=True, blank=True)
    exp_gain = models.CharField(max_length=100, null=True, blank=True)
    reps = models.CharField(max_length=100, null=True, blank=True)
    sets = models.CharField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.exercise_name} - {self.date_created}"
    
class GeneratePlan(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    exercise_name = models.CharField(max_length=500, null=True, blank=True)
    exercise_type = models.CharField(max_length=500, null=True, blank=True)
    muscle_group = models.CharField(max_length=500, null=True, blank=True)
    difficulty = models.CharField(max_length=500, null=True, blank=True)
    equipment = models.CharField(max_length=500, null=True, blank=True)
    instructions = models.CharField(max_length=2000, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plan - {self.exercise_name} - {self.date_created}"