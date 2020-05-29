from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import *
from .models import *
# Create your views here.

def xrayInput(request):

	if request.method == 'POST':
		form = XrayForm(request.POST, request.FILES)
		if form.is_valid():
			xrayObject = form.save()

		#return HttpResponseRedirect(reverse('classify', args=(gesture.id,)))
	else:
		form = XrayForm()
	return render(request, 'samplexray/index.html', {'form' : form})
