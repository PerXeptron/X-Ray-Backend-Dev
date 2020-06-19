from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

# Create your views here.

from .forms import XrayForm
from .models import XRaySample
from .dictionary import Dictionary

from keras.models import load_model
from keras.preprocessing import image
import keras.backend.tensorflow_backend as tb
import tensorflow as tf
from keras.applications.densenet import preprocess_input
import h5py
import numpy as np
import os

CURRENT_PATH = os.getcwd()
MODEL_PATH = os.path.join(CURRENT_PATH + "/models/densenet121-keras-3.h5")
ANOMALY_INDICES = {0 : 'Atelectasis', 1 : 'Cardiomegaly', 2 : 'Consolidation', 3 : 'Edema', 4 : 'Pleural Effusion'}

def index(request):
    return render(request, 'samplexray/index.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log in the user too !
            return redirect("samplexray:login")
    else:
        form = UserCreationForm()
    return render(request, 'samplexray/signup.html', {'form' : form})


def login(request):

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return HttpResponseRedirect(reverse('samplexray:profile', args=(user.id,)))
    else:
        form = AuthenticationForm()
    return render(request, 'samplexray/login.html', {'form' : form})

@login_required(login_url='/samplexray/login/')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('samplexray:index'))

def return_prediction(file_path):
	tb._SYMBOLIC_SCOPE.value = True
	xray_classifier_model = tf.keras.models.load_model(MODEL_PATH, compile=False)
	"""
	loaded_image = image.load_img(file_path, target_size=(224, 224))
	img_tensor = image.img_to_array(loaded_image)[:,:,:3]
	img_tensor = np.expand_dims(img_tensor, axis=0)
	img_tensor = imagenet_utils.preprocess_input(img_tensor)
	"""
	img = image.load_img(file_path, target_size=(224, 224))
	x = image.img_to_array(img).astype('float32')
	x = np.expand_dims(x, axis=0)
	x = preprocess_input(x)
	
	prediction = xray_classifier_model.predict(x)
	print(prediction)
	return prediction


@login_required(login_url='/samplexray/login/')
def profile(request, user_id):
    if(user_id == request.user.id):
        user = get_object_or_404(User, pk=user_id)
        pastxrays = user.xraysample_set.all().order_by('-date_posted')
        return render(request, 'samplexray/profile.html', {"user" : user, 'pastxrays' : pastxrays})
    else:
        return HttpResponse("Bad Request")


@login_required(login_url='/samplexray/login/')
def xrayupload(request, user_id):

	if(user_id == request.user.id):
		user = get_object_or_404(User, pk=user_id)
		if request.method == 'POST':
			form = XrayForm(request.POST, request.FILES)
			if form.is_valid():
				xrayTitle = form.cleaned_data['title']
				xrayImage = form.cleaned_data['image']
				xrayUser = user
				xrayDate_posted = timezone.now()

				newxray = XRaySample(title = xrayTitle, date_posted = xrayDate_posted, userperson = xrayUser, image = xrayImage,)
				newxray.save()

				disease_preds = return_prediction(os.path.join(CURRENT_PATH + newxray.image.url))
				#newxray.cool, newxray.fist, newxray.ok, newxray.stop, newxray.yo = disease_preds[0]
				newxray.atelectasis, newxray.cardiomegaly, newxray.consolidation, newxray.edema, newxray.pleural_effusion = disease_preds[0]
				newxray.save()
				
				return render(request, 'samplexray/result.html', {'xrayobj' : newxray, 'prediction' : disease_preds, 'anomaly_indices' : ANOMALY_INDICES})
				#return HttpResponseRedirect(reverse('samplexray:predict', args=(user.id, newxray.id,)))
		else:
			form = XrayForm()

		return render(request, 'samplexray/upload.html', {'form' : form, 'user' : user})

def xrayanonupload(request):
	if request.method == 'POST':
		form = XrayForm(request.POST, request.FILES)
		if form.is_valid():
			xrayTitle = form.cleaned_data['title']
			xrayImage = form.cleaned_data['image']
			
			path = default_storage.save(os.path.join('images/' + xrayTitle + '.jpg'), ContentFile(xrayImage.read()))
			display_path = os.path.join(settings.MEDIA_URL , path)
			tmp_file = os.path.join(settings.MEDIA_ROOT , path)

			prediction = return_prediction(tmp_file)
			
			return render(request, 'samplexray/anonresult.html', {'xraytitle' : xrayTitle, 'xrayimgurl' : display_path, 'prediction' : prediction, 'anomaly_indices' : ANOMALY_INDICES})
	else:
		form = XrayForm()
	return render(request, 'samplexray/anonupload.html', {'form' : form})

"""
@login_required(login_url='/samplexray/login/')
def predict(request, user_id, xray_id):

	xraysampleobj = get_object_or_404(XRaySample, pk=xray_id)
	if request.user.id == xraysampleobj.userperson.id:
		prediction = return_prediction(os.path.join(CURRENT_PATH + xraysampleobj.image.url))

		return render(request, 'samplexray/result.html', {'xrayobj' : xraysampleobj, 'prediction' : prediction, 'anomaly_indices' : ANOMALY_INDICES})
	else :
		return HttpResponse("Un-Authorized BAD REQUEST")
"""


"""
def anonpredict(request, xray_id):

	xraysampleobj = get_object_or_404(XRaySample, pk=xray_id)
	if xraysampleobj.userperson.id == 1 or request.user.id == xraysampleobj.userperson.id:
		cwd = os.getcwd()
		path = os.path.join(cwd + "\\Gestures_CNN_4_fine_tuned_mulltilabel.h5")
		tb._SYMBOLIC_SCOPE.value = True
		xray_classifier_model = tf.keras.models.load_model(path, compile=False)

		loaded_image = image.load_img(os.path.join(cwd + xraysampleobj.image.url), target_size=(224, 224), color_mode='rgb')
		img_tensor = image.img_to_array(loaded_image)[:,:,:3]
		img_tensor = np.expand_dims(img_tensor, axis=0)
		img_tensor /= 255.
		prediction = xray_classifier_model.predict(img_tensor)

		anomaly_indices = {0 : 'cool', 1 : 'fist', 2 : 'ok', 3 : 'stop', 4 : 'yo'}

		predict = np.argmax(prediction)
		gestureclass = anomaly_indices[predict]
		return render(request, 'samplexray/anonresult.html', {'xrayobj' : xraysampleobj, 'prediction' : prediction, 'anomaly_indices' : anomaly_indices})
	else :
		return HttpResponse("Un-Authorized BAD REQUEST")
"""