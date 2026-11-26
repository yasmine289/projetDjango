from django.contrib import admin
from .models import Appointment
# Register your models here.
#admin.site.register(Appointment)
@admin.register(Appointment)
class AppointmentAdminPerso(admin.ModelAdmin):
    list_display = (
        'id', 'reason', 'status',
         'appointment_date',
        'doctor', 'patient',
    )
    list_filter = ('status',)
    list_editable = ('status',)
    search_fields = ('duration_minutes',
'doctor__username',)
    list_per_page = 2
    ordering = ('appointment_date',)


