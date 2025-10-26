from django.contrib import admin
from .models import Doctor, Patient , Receptionist,Appointment

# Register your models to appear in Django admin
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Receptionist)
admin.site.register(Appointment)
