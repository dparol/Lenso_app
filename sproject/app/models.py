

# Create your models here.
from distutils.command.upload import upload
from django.db import models

# Create your models here.
class card(models.Model):
    card_name=models.TextField(max_length=100)
    card_text=models.CharField(max_length=100)
    card_img=models.ImageField(upload_to='upload')

    def __str__(self):
        return self.card_name