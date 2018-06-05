from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^statistics/', views.statisticsView, name='statistics'),
]
