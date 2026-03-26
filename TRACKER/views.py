from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import JobApplicationForm, CompanyForm, ResumeForm
from .models import Company, JobApplication, Resume
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import JobApplicationSerializer


@login_required
def home(request):
    applications = JobApplication.objects.filter(user=request.user)

    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        'applications': applications,
        'applied_count': applications.filter(status='Applied').count(),
        'interview_count': applications.filter(status='Interview').count(),
        'rejected_count': applications.filter(status='Rejected').count(),
        'offer_count': applications.filter(status='Offer').count(),
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
        'resume_form': resume_form,
        'page_title': 'Add Job Application',
        'submit_label': 'Save',
    })


@login_required
def edit_application(request, id):
    application = get_object_or_404(JobApplication, id=id, user=request.user)
    company_instance = application.company
    resume_instance = application.resume

    if request.method == 'POST':
        job_form = JobApplicationForm(request.POST, instance=application)
        company_form = CompanyForm(request.POST, instance=company_instance)

        if resume_instance:
            resume_form = ResumeForm(request.POST, request.FILES, instance=resume_instance)
        else:
            resume_form = ResumeForm(request.POST, request.FILES)

        if job_form.is_valid() and company_form.is_valid() and resume_form.is_valid():
            company = company_form.save()
            job = job_form.save(commit=False)
            job.user = request.user
            job.company = company

            if resume_form.cleaned_data.get('title') and (
                resume_form.cleaned_data.get('file') or resume_instance
            ):
                resume = resume_form.save()
                job.resume = resume

            job.save()
            messages.success(request, "Job application updated successfully!")
            return redirect('home')
    else:
        job_form = JobApplicationForm(instance=application)
        company_form = CompanyForm(instance=company_instance)
        resume_form = ResumeForm(instance=resume_instance) if resume_instance else ResumeForm()

    return render(request, 'add_application.html', {
        'job_form': job_form,
        'company_form': company_form,
        'resume_form': resume_form,
        'page_title': 'Edit Job Application',
        'submit_label': 'Update',
    })


@login_required
@require_POST
def delete_application(request, id):
    application = get_object_or_404(
        JobApplication,
        id=id,
        user=request.user
    )

    application.delete()
    messages.success(request, "Job application deleted successfully!")
    return redirect('home')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_list_api(request):
    jobs = JobApplication.objects.filter(user=request.user).select_related('company', 'resume')
    serializer = JobApplicationSerializer(jobs, many=True)
    return Response(serializer.data)


class JobStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        jobs = JobApplication.objects.filter(user=user)
        total = jobs.count()
        stats = jobs.values('status').annotate(count=Count('status'))

        status_dict = {
            "applied": 0,
            "interview": 0,
            "offer": 0,
            "rejected": 0
        }

        for item in stats:
            key = str(item['status']).lower()
            if key in status_dict:
                status_dict[key] = item['count']

        return Response({
            "total": total,
            **status_dict
        })
