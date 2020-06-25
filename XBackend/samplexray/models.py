from .dictionary import Dictionary

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

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
	heatmap_image = models.ImageField(upload_to='heatmaps/', null = False, blank = True)

	
	cardiomegaly = models.FloatField(default = 0.0)
	edema = models.FloatField(default = 0.0)
	consolidation = models.FloatField(default = 0.0)
	atelectasis = models.FloatField(default = 0.0)
	pleural_effusion = models.FloatField(default = 0.0)

	"""
	cool = models.FloatField(default = 0.0)
	fist = models.FloatField(default = 0.0)
	ok = models.FloatField(default = 0.0)
	stop = models.FloatField(default = 0.0)
	yo = models.FloatField(default = 0.0)
	"""
	#"Cardiomegaly", "Edema", "Consolidation", "Atelectasis", "Pleural Effusion"
	def __str__(self):
		return self.title

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)