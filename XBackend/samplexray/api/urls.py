from django.urls import path
#from rest_framework.authtoken.views import obtain_auth_token

from samplexray.api.views import (
    registration_view,
    custom_obtain_auth_token,
    api_detail_user_view,
    api_detail_xray_view,
    api_upload_xray_view,
    api_anonupload_xray_view,
    )

app_name = 'samplexray'

urlpatterns = [
    path('xray/', api_detail_xray_view, name='api-xraydetail'),
    path('user/', api_detail_user_view, name='api-userdetail'),
    path('login/', custom_obtain_auth_token, name='api-login'),
    path('signup/', registration_view, name='api-signup'),
    path('upload/', api_upload_xray_view, name='api-upload'),
    path('anonupload/', api_anonupload_xray_view, name='api-anonupload'),
]