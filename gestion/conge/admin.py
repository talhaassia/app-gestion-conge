
from django.contrib import admin
from .models import Personne, Conge

@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display = ('email', 'numposte', 'nom', 'prenom', 'cin', 'date_naissance', 'lieu_naissance', 'adresse', 'telephone', 'situation_familiale', 'nombre_enfant', 'date_recrutement', 'username')

@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display = ('type_de_conge', 'dureemax')

