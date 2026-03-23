from django import forms
from .models import JobApplication, Company, Resume


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['role', 'status', 'notes']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location']


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'file']