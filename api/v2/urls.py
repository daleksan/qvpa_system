from django.conf.urls import url

import api.v2.views

RG_AUTH = r'^auth/$'

urlpatterns = [
    # Auth
    url(RG_AUTH, api.v2.views.auth),
]
