from django.db import models

# Create your models here.


class TouristDestination(models.Model):
    Place_name=models.CharField(max_length=250)
    Weather=models.CharField(max_length=250)
    Location=models.CharField(max_length=250)
    State=models.CharField(max_length=250)
    District=models.CharField(max_length=250)
    Google_Map_Link=models.CharField(max_length=250)
    Image=models.ImageField(upload_to='Destination/')
    Description=models.CharField(max_length=5000)
