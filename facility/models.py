from django.db import models
from django.contrib.auth.models import User
from stdimage import StdImageField

from users.models import Profile

# Create your models here.

class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Facility (models.Model):
    name =  models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    rate = models.DecimalField(max_digits=6, decimal_places=2)
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
        return self.name

class Reservation(models.Model):
    STRAND = [('SUCCESS', 'SUCCESS'), ('PENDING FOR CANCELLATION', 'PENDING FOR CANCELLATION'), ('CANCELLED', 'CANCELLED')]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=STRAND, default='SUCCESS')
    date = models.DateField()
    start_time =  models.TimeField(auto_now=False, auto_now_add=False)
    end_time =  models.TimeField(auto_now=False, auto_now_add=False)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    cancelation_note = models.CharField(max_length=300)
    
    def __str__(self):
        return f'{self.facility} by {self.user}'