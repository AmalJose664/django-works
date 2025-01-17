from django.db import models
from django.utils import timezone




# Create your models here.

	


class Movie(models.Model):
	movie_name = models.CharField( max_length=80)
	movie_year = models.IntegerField()
	movie_rate = models.IntegerField()
	movie_addeddate = models.DateTimeField( default=timezone.now)
	movie_summary =models.TextField()

	def __str__(self):
		return self.movie_name
	

