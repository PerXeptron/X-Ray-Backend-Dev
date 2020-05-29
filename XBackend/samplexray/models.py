from django.db import models

# Create your models here.
"""
def upload_location(instance, filename, **kwargs):
	file_path = 'chex/anon/'
"""

class XRaySample(models.Model):
	title = models.CharField(max_length = 50, null = False, blank = False)
	image = models.ImageField(upload_to='images/', null = False, blank = False)
	date_posted = models.DateTimeField(auto_now_add = True, verbose_name = "date posted")
	slug = models.SlugField(blank = True, unique = True)

	def __str__(self):
		return self.title
