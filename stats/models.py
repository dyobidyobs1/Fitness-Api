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
        ("M", "Male"),
        ("F", "Female"),
    )

    gender = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    birth_date = models.CharField(max_length=50, null=True, blank=True)

