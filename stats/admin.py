from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models

class UserAdminConfig(UserAdmin):
    model = CustomUser
    search_fields = ('username', 'email')
    list_filter = ('first_name', 'is_active', 'is_staff', 'gender', 'birth_date')
    list_display = ('username', 'id', 'email','is_active', 'is_staff', 'gender', 'birth_date')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'gender', 'birth_date')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})}
    }
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'gender', 
                    'birth_date',
                    'is_active',
                    'is_staff',
                ),
            },
        ),
    )


admin.site.register(CustomUser, UserAdminConfig)
admin.site.register(Exercise)
admin.site.register(Stats)
admin.site.register(History)
