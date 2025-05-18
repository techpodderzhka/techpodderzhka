from django import forms
from .models import Form


class FormSubmissionForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ["name", "email", "phone", "category", "comment"]
