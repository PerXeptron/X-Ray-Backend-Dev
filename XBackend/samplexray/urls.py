from django.urls import path

from . import views


app_name = 'samplexray'
urlpatterns = [
    path('', views.xrayInput, name='index'),
]
