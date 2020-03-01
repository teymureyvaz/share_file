from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class File(models.Model):
	owner_id = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	description  = models.CharField(max_length=500)
	file = models.FileField(null=True,upload_to ='files/')
	expiration_date = models.DateField(null=True)


class UserFile(models.Model):
	file_id = models.ForeignKey(File,on_delete=models.CASCADE)
	shared_user_id = models.ForeignKey(User,on_delete=models.CASCADE)
