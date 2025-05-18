from django.db import models

# Create your models here.


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.CharField(max_length=64)

    class Meta:
        db_table = "employee"
        permissions = [
            ("can_assign_form", "Can assign forms to employees"),
        ]

    def __str__(self):
        return f"{self.name} {self.surname}"


class Form(models.Model):
    CATEGORY_CHOICES = [
        ("Проблемы с интернетом", "Проблемы с интернетом"),
        (
            "Проблемы с периферийным оборудованием",
            "Проблемы с периферийным оборудованием",
        ),
        ("Проблемы с электронной почтой", "Проблемы с электронной почтой"),
        ("Другие проблемы", "Другие проблемы"),
    ]
    STATUS_CHOICES = [
        ("обрабатывается", "обрабатывается"),
        ("не назначен", "не назначен"),
        ("завершен", "завершен"),
    ]

    form_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    category = models.CharField(
        max_length=64, choices=CATEGORY_CHOICES, null=True, blank=True
    )
    comment = models.CharField(max_length=200)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="не назначен"
    )

    class Meta:
        db_table = "form"

    def __str__(self):
        return f"{self.name} ({self.email})"


class FormAssignment(models.Model):
    STATUS_CHOICES = [
        ("не назначен", "не назначен"),
        ("обрабатывается", "обрабатывается"),
        ("завершен", "завершен"),
    ]

    assignment_id = models.AutoField(primary_key=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="не назначен"
    )
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "form_assignment"
        unique_together = ("form", "employee")

    def __str__(self):
        return f"Assignment #{self.assignment_id} - Form {self.form_id} to Employee {self.employee_id}"
