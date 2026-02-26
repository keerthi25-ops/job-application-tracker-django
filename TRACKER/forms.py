from django import forms
from .models import JobApplication, Company


class JobApplicationForm(forms.ModelForm):
    company_name = forms.CharField(label="Company")

    class Meta:
        model = JobApplication
        fields = ['company_name', 'role', 'status', 'resume', 'notes']
        # applied_date auto-created
        # user assigned in view

    def save(self, commit=True):
        company_name = self.cleaned_data['company_name']

        company, created = Company.objects.get_or_create(
            name=company_name
        )

        instance = super().save(commit=False)
        instance.company = company

        if commit:
            instance.save()

        return instance