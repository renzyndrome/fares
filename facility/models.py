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

class Service (models.Model):
    name =  models.CharField(max_length=200)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    def __str__(self):
        return f'{self.name} - P{self.price}'


class Facility (models.Model):
    name =  models.CharField(max_length=50)
    description = models.CharField(max_length=300, null=True, blank=True)
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    capacity = models.IntegerField(null=True, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    image = StdImageField(default='court.png', upload_to='facility', blank=True, variations={'large': (1280, 720), 'thumbnail': (640, 480, True)})
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.name

class Vehicle(models.Model):
    name = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=100)
    plate_num = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    capacity = models.IntegerField(null=True, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    image = StdImageField(default='court.png', upload_to='facility', blank=True, variations={'large': (1280, 720), 'thumbnail': (640, 480, True)})

    def __str__(self):
        return self.name
        
class Reservation(models.Model):
    STATUS = [('SUCCESS', 'SUCCESS'), ('PENDING PAYMENT', 'PENDING PAYMENT'), ('PENDING FOR CANCELLATION', 'PENDING FOR CANCELLATION'), ('CANCELLED', 'CANCELLED')]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STATUS, default='PENDING PAYMENT')
    start_time =  models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    duration = models.IntegerField()
    end_time =  models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    total_amount = models.IntegerField()
    cancellation_note = models.CharField(max_length=300, null=True, blank=True)
    
    class Meta:
        abstract = True
    

class FacilityReservation(Reservation):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    add_half_hour = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'{self.facility} by {self.user}'

class VehicleReservation(Reservation):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    purpose = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    starting_place = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    num_passengers = models.IntegerField(default=1)
    driver = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.vehicle} by {self.user}'

class Gallery(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    image = StdImageField(default='court.png', upload_to='facility', blank=True, variations={'large': (1280, 720), 'thumbnail': (640, 480, True)})