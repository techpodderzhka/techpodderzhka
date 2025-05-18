from django.contrib import admin
from .models import Form, FormAssignment, Employee

# Register your models here.

admin.site.register(Form)
admin.site.register(FormAssignment)
admin.site.register(Employee)
