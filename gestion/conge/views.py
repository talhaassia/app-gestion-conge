from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .form import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Conge, LeaveRequest, Personne
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .form import LeaveRequestForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Max
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.conf import settings
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from django.template.loader import get_template
from xhtml2pdf import pisa
import os

# Create your views here.
def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique de l'utilisateur après l'inscription
            if user.is_director:
                return redirect('directeur_home')  # Redirection vers l'accueil du directeur
            else:
                return redirect('employe_home')  # Redirection vers l'accueil de l'employé
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_director:
                    return redirect('directeur_home')  # Redirection vers l'accueil du directeur
                else:
                    return redirect('employe_home')  # Redirection vers l'accueil de l'employé
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Formulaire invalide. Veuillez vérifier les informations saisies.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'connexion.html', {'form': form})

@login_required
def directeur_home(request):
    user = request.user
    if user.is_director:
        return render(request, 'directeur_home.html', {'user': user})
    else:
        return redirect('employe_home')

@login_required
def employe_home(request):
    user = request.user
    if not user.is_director:
        return render(request, 'employe_home.html', {'user': user})
    else:
        return redirect('directeur_home')
@login_required
def processing_requests_view(request):
    # Vérifiez si l'utilisateur est un directeur
    if hasattr(request.user, 'is_director') and request.user.is_director:
        # Récupère toutes les demandes de congé à traiter
        requests = LeaveRequest.objects.filter(traitement=False)
        # Rend le template avec les données
        return render(request, 'processing_requests.html', {'requests': requests})
    else:
        # Redirigez l'utilisateur s'il n'est pas directeur
        return redirect('directeur_home')
@login_required
def processed_requests_view(request):
    # Vérifiez si l'utilisateur est un directeur
    if hasattr(request.user, 'is_director') and request.user.is_director:
        # Récupère toutes les demandes de congé traitées
        requests = LeaveRequest.objects.filter(traitement=True)
        # Logique de traitement supplémentaire peut être ajoutée ici si nécessaire

        # Rend le template avec les données
        return render(request, 'processed_requests.html', {'requests': requests})
    else:
        # Redirigez l'utilisateur s'il n'est pas directeur
        return redirect('directeur_home')

@login_required
def create_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.save()
            messages.success(request, "Votre demande de congé a été soumise avec succès.")
            return redirect('employe_home')
        else:
            messages.error(request, "Il y a une erreur dans le formulaire. Veuillez vérifier les champs.")
    else:
        form = LeaveRequestForm()

    return render(request, 'create_leave_request.html', {'form': form})

def view_leave_requests(request):
    leave_requests = LeaveRequest.objects.filter(personne=request.user)
    latest_requests = leave_requests.order_by('date_debut').values('id', 'date_debut', 'date_fin', 'type_conge', 'motif', 'statut')
    leave_requests_list = list(latest_requests)
    context = {'leave_requests': leave_requests_list}
    return render(request, 'view_leave_status.html', context)

def generate_leave_pdf(request, request_id):
    # Retrieve the leave request and the employee
    leave_request = get_object_or_404(LeaveRequest, id=request_id)
    employee = leave_request.personne
    
    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="leave_request_{request_id}.pdf"'

    # Create a template with dynamic content
    template = get_template('leave_request_template.html')
    context = {
        'leave_request': leave_request,
        'employee': employee,
    }
    html = template.render(context)

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Return the PDF response
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def deconnexion(request):
    logout(request)
    return redirect('connexion')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')

@login_required
def password_change_done(request):
    return render(request, 'password_change_done.html')

@require_POST
def approve_request(request, request_id):
    leave_request = get_object_or_404(LeaveRequest, id=request_id)
    leave_request.statut = 'approved'
    leave_request.traitement = True
    leave_request.save()
    return redirect('processing_requests')

@require_POST
def reject_request(request, request_id):
    leave_request = get_object_or_404(LeaveRequest, id=request_id)
    leave_request.statut = 'rejected'
    leave_request.traitement = True
    leave_request.save()
    return redirect('processing_requests')