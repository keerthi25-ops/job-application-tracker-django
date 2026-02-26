from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_application, name='add_application'),
    path('edit/<int:id>/',views.edit_application, name='edit_application'),
    path('delete/<int:id>/',views.delete_application, name='delete_application'),

     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    
    path('logout/', views.user_logout, name='logout'),
    path('api/jobs/', views.job_list_api, name='job_list_api'),
    path('register/', views.register, name='register'),
    path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'
    ),
    name='password_reset'
),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),


    ]