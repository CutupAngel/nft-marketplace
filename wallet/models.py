from django.db import models


# Create your models here.
class User(models.Model):
    address = models.CharField(max_length=100)
    fileType = models.CharField(max_length=100)
    fileName = models.CharField(max_length=100, blank=True)
    fileId = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"


class File(models.Model):
    token_id = models.IntegerField(max_length=10)
    token_portion = models.TextField()
    fileId = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "file"
