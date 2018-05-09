# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import Setting


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        exclude = ('id', 'user')


class UserSerializer(serializers.ModelSerializer):
    settings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_staff', 'settings')

    def get_settings(self, obj):
        try:
            obj = Setting.objects.get(user_id=obj.id)
        except Setting.DoesNotExist:
            return None
        else:
            return UserSettingsSerializer(obj).data
