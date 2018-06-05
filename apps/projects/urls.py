from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^projects/', views.projectsView, name='projects'),
]
