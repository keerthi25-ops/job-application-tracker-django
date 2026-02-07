from django.contrib import admin
from .models import  Company, Resume, JobApplication
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'status', 'applied_date', 'user')
    readonly_fields = ('applied_date',)


admin.site.register(Company)
admin.site.register(Resume)
admin.site.register(JobApplication, JobApplicationAdmin)




