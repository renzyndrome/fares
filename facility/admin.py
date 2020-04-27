from django.contrib import admin

# Register your models here.

from .models import Facility, Service, Tag, Reservation, Gallery
from users.models import Profile
from users.admin import ProfileAdmin


class InlineReservation(admin.TabularInline):
    model = Reservation
    extra = 1

class InlineGallery(admin.TabularInline):
    model = Gallery
    extra = 1

class ProfileAdmin(ProfileAdmin):
    inlines = [InlineReservation]


# ProfileAdmin.inlines.append(InlineReservation)

class FacilityAdmin(admin.ModelAdmin):
    inlines = [InlineReservation, InlineGallery]
    list_display = ('name', 'capacity', 'rate')
    list_filter = ('name', 'capacity')
    ordering = ('name',)
    search_fields = ('name',)
    fieldsets = (
        (Facility, {
            'fields': ('name','image','description','tags', 'rate', 'isVehicle',)
        }),
        ('Additional Info', {
            'classes': ('collapse',),
            'fields': ('capacity',),
        }),
    )

class ReservationAdmin(admin.ModelAdmin):
    readonly_fields = ['total_amount']
    list_display = [field.name for field in Reservation._meta.get_fields() if field.name != 'services']

class GalleryAdmin(admin.ModelAdmin):
    model = Gallery

admin.site.register(Facility, FacilityAdmin)
admin.site.register(Service)
admin.site.register(Tag)
admin.site.register(Reservation, ReservationAdmin)
admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Gallery, GalleryAdmin)