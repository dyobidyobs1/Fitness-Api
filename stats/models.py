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



class Exercise(models.Model):
    exercise_name = models.CharField(max_length=100, null=True, blank=True)
    exp_gain = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/excercise', blank=True, null=True)


    def __str__(self):
        return f"{self.exercise_name}"