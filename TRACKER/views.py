from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobApplicationForm
from .models import JobApplication
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobApplicationSerializer



@login_required
def home(request):
    applications = JobApplication.objects.filter(user=request.user)
    status_filter = request.GET.get('status')

    if status_filter:
        applications = applications.filter(status=status_filter)

    applied_count = applications.filter(status='Applied').count()
    interview_count = applications.filter(status='Interview').count()
    rejected_count = applications.filter(status='Rejected').count()
    offer_count = applications.filter(status='Offer').count()

    context = {
        'applications': applications,
        'applied_count': applied_count,
        'interview_count': interview_count,
        'rejected_count': rejected_count,
        'offer_count': offer_count,
    }
    return render(request, 'home.html', context)


@login_required
def add_application(request):
    form = JobApplicationForm(request.POST or None)
    if form.is_valid():
        job = form.save(commit=False)
        job.user = request.user
        job.save()
        return redirect('home')
    return render(request, 'add_application.html', {'form': form})


@login_required
def edit_application(request, id):
    application = get_object_or_404(JobApplication, id=id)
    form = JobApplicationForm(request.POST or None, instance=application)
    if form.is_valid():
        job = form.save(commit=False)
        job.user = application.user
        job.save()
        return redirect('home')
    return render(request, 'add_application.html', {'form': form})


@login_required
def delete_application(request, id):
    application = get_object_or_404(JobApplication, id=id)
    application.delete()
    return redirect('home')


def user_logout(request):
    logout(request)
    return redirect('/login/')

@api_view(['GET'])
def job_list_api(request):
    jobs = JobApplication.objects.all()
    serializer = JobApplicationSerializer(jobs, many=True)
    return Response(serializer.data)
