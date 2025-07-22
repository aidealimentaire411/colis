from django.db import models
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError


# TABLE : Année scolaire (créée par l'admin)
class AnneeScolaire(models.Model):
    libelle = models.CharField(max_length=20, unique=True)  # ex: "2025-2026"
    active = models.BooleanField(default=False)  # une seule année active à la fois

    def __str__(self):
        return self.libelle

# TABLE : Symbole (créé par admin ou par script initial)
class Symbole(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    icone = models.CharField(max_length=10)  # emoji

    def __str__(self):
        return f"{self.icone} {self.nom}"



# TABLE : Étudiant
class Etudiant(models.Model):

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    carte_etudiant = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    symbole = models.ForeignKey(Symbole, on_delete=models.SET_NULL, null=True, editable=False)
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.PROTECT, editable=False)
    date_inscription = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)  # Désactivé par défaut

    def save(self, *args, **kwargs):
        if not self.annee_scolaire_id:
            self.annee_scolaire = AnneeScolaire.objects.get(active=True)

        if not self.symbole_id:
            tous_les_symboles = list(Symbole.objects.all())
            compteur = {s.id: Etudiant.objects.filter(symbole=s).count() for s in tous_les_symboles}
            symbole_le_moins_utilise = min(compteur, key=compteur.get)
            self.symbole = Symbole.objects.get(id=symbole_le_moins_utilise)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Passage(models.Model):
    etudiant = models.ForeignKey("Etudiant", on_delete=models.CASCADE, related_name='passages')
    date_passage = models.DateTimeField(blank=True, null=True)  # Plus d'auto_now_add

    def clean(self):
        # Si pas encore défini, prendre la date actuelle (utilisé en validation)
        date_ref = self.date_passage or timezone.now()

        debut_jour = date_ref.replace(hour=0, minute=0, second=0, microsecond=0)
        fin_jour = date_ref.replace(hour=23, minute=59, second=59, microsecond=999999)

        if Passage.objects.filter(
            etudiant=self.etudiant,
            date_passage__range=(debut_jour, fin_jour)
        ).exclude(id=self.id).exists():
            raise ValidationError("Un passage existe déjà pour cet étudiant aujourd'hui.")

    def save(self, *args, **kwargs):
        if not self.date_passage:
            self.date_passage = timezone.now()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.etudiant} - {self.date_passage.strftime('%d/%m/%Y %H:%M')}"
