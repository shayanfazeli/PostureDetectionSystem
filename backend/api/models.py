from django.db import models

class Histogram(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField()
	is_bad_posture = models.BooleanField()