from django.db import models
from django.utils import timezone

# Create your models here.
class MessageSetting(models.Model):
	username = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	body = models.TextField()
	interval = models.IntegerField()
	
class MessageSent(models.Model):
	sender = models.CharField(max_length=30)
	receiver = models.CharField(max_length=30)
	message = models.TextField()
	datetime = models.DateTimeField(default=timezone.now)
