from django.contrib import admin

# Register your models here.

from .models import Facility, Vehicle, Service, Tag, Reservation, FacilityReservation, VehicleReservation
from users.models import Profile
from users.admin import ProfileAdmin


class InlineFacilityReservation(admin.TabularInline):
    model = FacilityReservation
    extra = 1



class ProfileAdmin(ProfileAdmin):
    inlines = [InlineFacilityReservation]


# ProfileAdmin.inlines.append(InlineReservation)

class FacilityAdmin(admin.ModelAdmin):
    # inlines = [InlineReservation]
    list_display = ('name', 'capacity', 'rate',)
    list_filter = ('name', 'capacity')
    ordering = ('name',)
    search_fields = ('name',)
 

class VehicleAdmin(admin.ModelAdmin):
    pass

# class ReservationAdmin(admin.ModelAdmin):
#     readonly_fields = ['total_amount']
#     list_display = [field.name for field in Reservation._meta.get_fields() if field.name != 'services']

class FacilityReservationAdmin(admin.ModelAdmin):
    list_display = ('facility', 'user', 'start_time', 'end_time', 'total_amount', 'status')

class VehicleReservationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'user', 'start_time', 'end_time', 'total_amount', 'status')

admin.site.register(Facility, FacilityAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Service)
admin.site.register(Tag)
# admin.site.register(Reservation, ReservationAdmin)
admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(FacilityReservation, FacilityReservationAdmin)
admin.site.register(VehicleReservation, VehicleReservationAdmin)