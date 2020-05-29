from django import forms
from .models import *

class XrayForm(forms.ModelForm):

	class Meta :
		model = XRaySample
		fields = ['title', 'image']