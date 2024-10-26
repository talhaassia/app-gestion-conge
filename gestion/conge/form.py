from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate
from .models import Personne, Conge, LeaveRequest

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    numposte = forms.CharField(required=True)
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)
    cin = forms.CharField(required=True)
    date_naissance = forms.DateField(required=True)
    lieu_naissance = forms.CharField(required=True)
    adresse = forms.CharField(required=True)
    telephone = forms.CharField(required=True)
    situation_familiale = forms.CharField(required=True)
    nombre_enfant = forms.IntegerField(required=True)
    date_recrutement = forms.DateField(required=True)
    is_director = forms.BooleanField(label='Directeur', required=False)
    
    class Meta(UserCreationForm.Meta):
        model = Personne
        fields = (
            "username", "password1", "password2", "email", "numposte", "nom", "prenom", 
            "cin", "date_naissance", "lieu_naissance", "adresse", "telephone", 
            "situation_familiale", "nombre_enfant", "date_recrutement",'is_director'
        )
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nom d\'utilisateur'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Mot de passe actuel', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nouveau mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirmer le nouveau mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')
class LeaveRequestForm(forms.ModelForm):
    type_conge = forms.ModelChoiceField(
        queryset=Conge.objects.all(), 
        label='Type de congé',
        required=True
    )
    date_debut = forms.DateField(
        label='Date de début', 
        widget=forms.TextInput(attrs={'type': 'date'}), 
        required=True
    )
    date_fin = forms.DateField(
        label='Date de fin', 
        widget=forms.TextInput(attrs={'type': 'date'}), 
        required=True
    )
    motif = forms.CharField(
        label='Motif', 
        widget=forms.Textarea(attrs={'rows': 3}), 
        required=True
    )
    personne = forms.ModelChoiceField(
        queryset=Personne.objects.all(),
        label="Nom complet de l'employé",
        required=True
    )

    class Meta:
        model = LeaveRequest
        fields = ['type_conge', 'date_debut', 'date_fin', 'motif', 'personne']