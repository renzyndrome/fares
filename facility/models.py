from django.db import models
from django.contrib.auth.models import User

from users.models import Profile

# Create your models here.
class Facility (models.Model):
    name =  models.CharField(max_length=200)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    isVehicle =  models.BooleanField(default=False)
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Service (models.Model):
    name =  models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return self.name

class Reservation(models.Model):
    STRAND = [('SUCCESS', 'SUCCESS'), ('PENDING FOR CANCELLATION', 'PENDING FOR CANCELLATION'), ('CANCELLED', 'CANCELLED')]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STRAND, default='SUCCESS')
    date = models.DateField()
    startTime =  models.TimeField(auto_now=False, auto_now_add=False)
    endTime =  models.TimeField(auto_now=False, auto_now_add=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.facility} by {self.user}'

