from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

from samplexray.models import XRaySample
from samplexray.api.serializers import XRaySampleSerializer, RegistrationSerializer
from samplexray.views import return_prediction

import os

CURRENT_PATH = os.getcwd()

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully Signed Up"
            data['username'] = user.username
            token = Token.objects.get(user=user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_detail_user_view(request):
    if request.method == "POST":
        logged_in_user = request.user
        try :
            user = User.objects.get(pk=request.data.get('user_id'))
        except User.DoesNotExist :
            return Response(status=status.HTTP_404_NOT_FOUND)

        if logged_in_user != user :
            return Response({'response' : "You don't have permission to view this."})

        user_pastxray_list = user.xraysample_set.all().order_by('-date_posted')
        data = {}
        data['username'] = user.username
        data['pastxrays'] = [xray_sample.id for xray_sample in user_pastxray_list]

        return Response(data)



@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_detail_xray_view(request):
    
    if request.method == "POST":
        try :
            xray_sample = XRaySample.objects.get(pk=request.data.get('xray_id'))
        except XRaySample.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        
        if xray_sample.userperson != user :
            return Response({'response' : "You don't have permission to view this."})

        serializer = XRaySampleSerializer(xray_sample)
        return Response(serializer.data)



@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_upload_xray_view(request):
    user = request.user
    xray_post = XRaySample(userperson=user)
    if request.method == 'POST' :
        serializer = XRaySampleSerializer(xray_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            prediction_list = return_prediction(os.path.join(CURRENT_PATH + xray_post.image.url))
            xray_post.cool, xray_post.fist, xray_post.ok, xray_post.stop, xray_post.yo = prediction_list[0]
            xray_post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST',])
def api_anonupload_xray_view(request):
    """
    Keeping first user as the anonymous user
    """
    anonuser = User.objects.get(pk=1)
    xray_post = XRaySample(userperson=anonuser)
    if request.method == 'POST' :
        serializer = XRaySampleSerializer(xray_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            prediction_list = return_prediction(os.path.join(CURRENT_PATH + xray_post.image.url))
            xray_post.cool, xray_post.fist, xray_post.ok, xray_post.stop, xray_post.yo = prediction_list[0]
            xray_post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)