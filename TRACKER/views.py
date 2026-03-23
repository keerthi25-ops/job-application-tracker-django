from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import JobApplicationForm, CompanyForm, ResumeForm
from .models import Company   # IMPORTANT
from django.contrib import messages

@login_required
def add_application(request):
    if request.method == 'POST':
        job_form = JobApplicationForm(request.POST)
        company_form = CompanyForm(request.POST)
        resume_form = ResumeForm(request.POST, request.FILES)

        if job_form.is_valid() and company_form.is_valid() and resume_form.is_valid():

            company, created = Company.objects.get_or_create(
                name=company_form.cleaned_data['name'],
                defaults={'location': company_form.cleaned_data['location']}
            )

            resume = resume_form.save()

            job = job_form.save(commit=False)
            job.user = request.user
            job.company = company
            job.resume = resume
            job.save()
            messages.success(request, "Job application added successfully!")


            return redirect('home')

        else:
            print(job_form.errors)
            print(company_form.errors)
            print(resume_form.errors)

    else:
        job_form = JobApplicationForm()
        company_form = CompanyForm()
        resume_form = ResumeForm()

    return render(request, 'add_application.html', {
        'job_form': job_form,
        'company_form': company_form,
        'resume_form': resume_form
    })