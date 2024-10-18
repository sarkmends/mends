from django.db import models


class ImageCategory(models.Model):
    name=models.CharField(max_length=255)

class Image(models.Model):
    name=models.CharField(max_length=255)
    file=models.ImageField(null=True,blank=True,upload_to='image/')
    category=models.ForeignKey(ImageCategory,on_delete=models.CASCADE)

# Create your models here.
