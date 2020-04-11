from django.db import models
from django.contrib.auth.models import User
from stdimage import StdImageField
from django.shortcuts import redirect


from users.models import Profile

# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Facility (models.Model):
    name =  models.CharField(max_length=50)
    description = models.CharField(max_length=300, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    isVehicle =  models.BooleanField(default=False)
    capacity = models.IntegerField(null=True, blank=True)
    image = StdImageField(default='court.png', upload_to='facility', blank=True, variations={'large': (1280, 720), 'thumbnail': (640, 480, True)})
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name


class Service (models.Model):
    name =  models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f'{self.name} - P{self.price}'



class Reservation(models.Model):
    STATUS = [('SUCCESS', 'SUCCESS'), ('PENDING FOR CANCELLATION', 'PENDING FOR CANCELLATION'), ('CANCELLED', 'CANCELLED')]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STATUS, default='SUCCESS')
    start_time =  models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    duration = models.IntegerField()
    add_half_hour = models.BooleanField()
    end_time =  models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    add_half_hour = models.BooleanField(null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cancellation_note = models.CharField(max_length=300, null=True, blank=True)
    
    def __str__(self):
        return f'{self.facility} by {self.user}'

class Gallery(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    image = StdImageField(default='court.png', upload_to='facility', blank=True, variations={'large': (1280, 720), 'thumbnail': (640, 480, True)})