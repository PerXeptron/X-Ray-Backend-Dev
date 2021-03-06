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

from keras.models import model_from_json
from keras.preprocessing import image
import keras.backend.tensorflow_backend as tb
import tensorflow as tf
from keras.applications.densenet import preprocess_input
import h5py
import numpy as np
import os

from .heatmap_utils import load_torch_model
from .heatmap_utils.generate_heatmap import HeatmapGenerator

from .ensemble_utils.ensemble import Ensemble

CURRENT_PATH = os.getcwd()
ANOMALY_INDICES = {0 : 'Atelectasis', 1 : 'Cardiomegaly', 2 : 'Consolidation', 3 : 'Edema', 4 : 'Pleural Effusion'}
ENSEMBLE_OBJECT_GLOBAL = None
PYTORCH_HEATMAP_MODEL = None

#SET TENSORFLOW ENVIRONMENT TO OPTIMAL
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)
tb._SYMBOLIC_SCOPE.value = True


"""
-------------------------
AUTHENTICATION AREA ---->
-------------------------
"""


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


"""
---------------------------------------
MODEL LOADING AND PREDICTION AREA ---->
---------------------------------------
"""


def load_pytorch_model():
	global PYTORCH_HEATMAP_MODEL
	PYTORCH_HEATMAP_MODEL = load_torch_model.build_model()
	print("PyTorch TarBall Loaded :p")


def generate_heatmap(input_file_path, output_file_path):
	global PYTORCH_HEATMAP_MODEL	

	if PYTORCH_HEATMAP_MODEL is None :
		print("WARNING : PYTORCH MODEL REQUIRED AGAIN MEMORY LEAKAGE !")
		PYTORCH_HEATMAP_MODEL = load_torch_model.build_model()

	h = HeatmapGenerator(PYTORCH_HEATMAP_MODEL)
	h.generate(input_file_path, output_file_path)


def load_ensemble_model():
	global ENSEMBLE_OBJECT_GLOBAL
	ENSEMBLE_OBJECT_GLOBAL = Ensemble()
	ENSEMBLE_OBJECT_GLOBAL.build_models()

def return_prediction(file_path):
	global ENSEMBLE_OBJECT_GLOBAL

	if ENSEMBLE_OBJECT_GLOBAL is None :
		ENSEMBLE_OBJECT_GLOBAL.build_models()

	return ENSEMBLE_OBJECT_GLOBAL.get_predictions(file_path)


"""
DJANGO TEMPLATES AREA --->
"""


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