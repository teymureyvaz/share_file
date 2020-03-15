from django.db import models
from django.contrib.auth.models import User
from main_project.models import File
# Create your models here.
from datetime import datetime as dt

class Comment(models.Model):
	author = models.ForeignKey(User,on_delete= models.CASCADE)
	text = models.TextField()
	file = models.ForeignKey(File,on_delete=models.CASCADE)
	publish_date= models.DateTimeField(blank=True,default=dt.now)
	is_active = models.BooleanField(default=True)
