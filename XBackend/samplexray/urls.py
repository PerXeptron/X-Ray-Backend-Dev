from django.urls import path

from . import views


app_name = 'samplexray'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/results/<int:xray_id>/', views.predict, name='predict'),
    path('results/<int:xray_id>/', views.anonpredict, name='anonpredict'),
    path('profile/<int:user_id>/upload/', views.xrayupload, name='upload'),
    path('upload/', views.xrayanonupload, name='anonupload'),
]
