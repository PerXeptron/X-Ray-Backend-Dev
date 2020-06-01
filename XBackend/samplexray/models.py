from django.db import models
from django.contrib.auth.models import User
from .dictionary import Dictionary
# Create your models here.
"""
def upload_location(instance, filename, **kwargs):
	file_path = 'chex/anon/'
"""

class XRaySample(models.Model):
	title = models.CharField(max_length = 50, null = False, blank = False)
	image = models.ImageField(upload_to='images/', null = False, blank = False)
	date_posted = models.DateTimeField(auto_now_add = True, verbose_name = "date posted")
	userperson = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
	#"Cardiomegaly", "Edema", "Consolidation", "Atelectasis", "Pleural Effusion"
	def __str__(self):
		return self.title
