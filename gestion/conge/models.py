from django.db import models
from django.contrib.auth.models import AbstractUser

class Personne(AbstractUser):
    email = models.EmailField(unique=True)
    numposte = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    cin = models.CharField(max_length=20, unique=True)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    situation_familiale = models.CharField(max_length=50)
    nombre_enfant = models.IntegerField()
    date_recrutement = models.DateField()
    username = models.CharField(max_length=150, unique=True)
    is_director = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='personne_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='personne',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='personne_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='personne',
    )
    def __str__(self):
        return f"{self.prenom} {self.nom} {self.username}"

class Conge(models.Model):
    CONGE_CHOICES = [
        ('exceptionnel', 'Exceptionnel'),
        ('maladie', 'Maladie'),
        ('repos', 'Repos'),
    ]
    type_de_conge = models.CharField(max_length=100, choices=CONGE_CHOICES, default='repos')
    dureemax = models.IntegerField()
    traitement = models.BooleanField(default=False)

    def __str__(self):
        return self.get_type_de_conge_display()  # Affiche le label au lieu de la valeur brute

class LeaveRequest(models.Model):
    type_conge = models.ForeignKey(Conge, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField(default='Pas de raison specifique')
    personne = models.ForeignKey(Personne, on_delete=models.CASCADE)
    statut = models.CharField(max_length=100, default='En attente')
    traitement = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Request by {self.personne} from {self.date_debut} to {self.date_fin}'
