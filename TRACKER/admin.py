from django.contrib import admin
from .models import  Company, Resume, JobApplication
class JobApplicationAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


admin.site.register(Company)
admin.site.register(Resume)
admin.site.register(JobApplication, JobApplicationAdmin)




