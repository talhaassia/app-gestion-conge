from django.contrib import admin
from django.urls import path
from conge import views
from conge.views import (
    CustomPasswordChangeView, password_change_done, create_leave_request, 
    view_leave_requests, generate_leave_pdf, approve_request, reject_request
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('directeur_home/', views.directeur_home, name='directeur_home'),
    path('employe_home/', views.employe_home, name='employe_home'),
    path('processing-requests/', views.processing_requests_view, name='processing_requests'),
    path('directeur/processed_requests/', views.processed_requests_view, name='processed_requests'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password-change-done/', password_change_done, name='password_change_done'),
    path('create-leave-request/', views.create_leave_request, name='create_leave_request'),
    path('view-requests/', views.view_leave_requests, name='view_leave_status'),
    path('generate-pdf/<int:request_id>/', views.generate_leave_pdf, name='generate_leave_pdf'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
