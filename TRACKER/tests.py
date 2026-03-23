from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Company, JobApplication, Resume


class TrackerViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')
        self.company = Company.objects.create(name='OpenAI', location='Remote')
        self.resume = Resume.objects.create(title='Main Resume', file='resumes/test.pdf')
        self.application = JobApplication.objects.create(
            user=self.user,
            company=self.company,
            role='Engineer',
            status='Applied',
            resume=self.resume,
        )

    def test_home_requires_login(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_home_shows_dashboard_counts(self):
        self.client.login(username='tester', password='secret123')
        JobApplication.objects.create(
            user=self.user,
            company=self.company,
            role='Researcher',
            status='Interview',
            resume=self.resume,
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['applied_count'], 1)
        self.assertEqual(response.context['interview_count'], 1)
        self.assertEqual(response.context['rejected_count'], 0)
        self.assertEqual(response.context['offer_count'], 0)

    def test_delete_application_requires_post(self):
        self.client.login(username='tester', password='secret123')

        response = self.client.get(reverse('delete_application', args=[self.application.id]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(JobApplication.objects.filter(id=self.application.id).exists())

    def test_job_api_returns_user_jobs(self):
        self.client.login(username='tester', password='secret123')

        response = self.client.get(reverse('job_list_api'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
