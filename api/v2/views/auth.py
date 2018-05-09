# -*- coding: utf-8 -*-
import logging
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from sso.diadice_ldap import DiadiceLDAP
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger()


class SessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class RemoteUserAuthentication(authentication.BaseAuthentication):
    create_unknown_user = True

    def authenticate(self, request):
        remote_user = request.META.get('HTTP_REMOTE_USER')
        if not remote_user:
            return None

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(username=remote_user)
        except UserModel.DoesNotExist:
            if self.create_unknown_user:
                user, created = UserModel._default_manager.get_or_create(**{
                    UserModel.USERNAME_FIELD: remote_user
                })
                if created:
                    user = self.configure_user(user)
            else:
                try:
                    user = UserModel._default_manager \
                        .get_by_natural_key(remote_user)
                except UserModel.DoesNotExist:
                    pass

        return (user, None)

    def configure_user(self, user):
        diadice_ldap = DiadiceLDAP(settings.DIADICE_LDAP_USERNAME,
                                   settings.DIADICE_LDAP_PASSWORD)
        try:
            user_info = diadice_ldap.get_user_info(user.username)
        except Exception, e:
            logger.warning("Failed to get user info: %s" % e)
        else:
            for k, v in user_info.iteritems():
                setattr(user, k, v)
            user.save()

        return user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_staff')


class AuthView(APIView):
    authentication_classes = (RemoteUserAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']

    def get(self, request):
        if self.request.user.is_authenticated():
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data)
        else:
            raise AuthenticationFailed
