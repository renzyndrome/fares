from django.contrib import admin

# Register your models here.

from .models import Facility
from .models import Service
from .models import Reservation

admin.site.register(Facility)
admin.site.register(Service)
admin.site.register(Reservation)