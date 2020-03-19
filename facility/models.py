from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Facility (models.Model):
    name =  models.CharField(max_length=200)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    isVehicle =  models.BooleanField(default=False)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

class Service (models.Model):
    name =  models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField()
    startTime =  models.TimeField(auto_now=False, auto_now_add=False)
    endTime =  models.TimeField(auto_now=False, auto_now_add=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)