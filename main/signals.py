from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee


@receiver(post_save, sender=User)
def sync_employee_with_user(sender, instance, **kwargs):
    if instance.groups.filter(name="employee").exists():
        employee, created = Employee.objects.get_or_create(username=instance.username)

        employee.name = instance.first_name
        employee.surname = instance.last_name
        employee.email = instance.email
        employee.save()
    else:
        Employee.objects.filter(username=instance.username).delete()
