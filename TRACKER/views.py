from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import JobApplicationForm, CompanyForm, ResumeForm
from .models import Company, JobApplication   # IMPORTANT
from django.contrib import messages
from django.shortcuts import get_object_or_404
@login_required
def home(request):
    applications = JobApplication.objects.filter(user=request.user)
    
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        'applications': applications,
    }
    return render(request, 'home.html', context)

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
@login_required
def edit_application(request, id):
    application = get_object_or_404(JobApplication, id=id, user=request.user)

    job_form = JobApplicationForm(request.POST or None, instance=application)

    if job_form.is_valid():
        job = job_form.save(commit=False)
        job.user = request.user
        job.save()
        return redirect('home')

    return render(request, 'add_application.html', {
        'job_form': job_form
    })