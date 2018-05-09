# -*- coding: utf-8 -*-
import logging

from django.contrib.auth.backends import \
    RemoteUserBackend as BaseRemoteUserBackend
from django.conf import settings
from diadice_ldap import DiadiceLDAP

logger = logging.getLogger()


class RemoteUserBackend(BaseRemoteUserBackend):
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
