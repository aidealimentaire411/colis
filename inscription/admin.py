from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django import forms
from .models import Etudiant, Symbole, AnneeScolaire, Passage
from datetime import datetime
from django.core.exceptions import ValidationError


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = '__all__'
        widgets = {
            'date_naissance': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'  # Ce format est requis pour l'affichage correct
            ),


        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_naissance'].input_formats = ['%Y-%m-%d']


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    form = EtudiantForm

    # 🆕 remplace 'date_naissance' par la méthode personnalisée
    list_display = (
    'nom', 'prenom', 'date_naissance_affiche', 'email', 'symbole', 'annee_scolaire', 'active', 'ajouter_passage_bouton')

    def date_naissance_affiche(self, obj):
        return obj.date_naissance.strftime('%d/%m/%Y')

    date_naissance_affiche.short_description = "Date de naissance"
    # 🔍 Recherche sur nom, prénom, email, carte étudiant
    search_fields = ('nom', 'prenom', 'email', 'carte_etudiant', 'date_naissance')

    # 🧮 Filtres dans la barre latérale
    list_filter = ('active', 'annee_scolaire', 'symbole')

    # 🔒 Champs non modifiables dans l’admin
    readonly_fields = ('symbole', 'annee_scolaire', 'date_inscription')

    # ➕ Bouton personnalisé
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:etudiant_id>/ajouter_passage/', self.admin_site.admin_view(self.ajouter_passage),
                 name='ajouter-passage'),
        ]
        return custom_urls + urls


    def ajouter_passage(self, request, etudiant_id):
        try:
            etudiant = Etudiant.objects.get(pk=etudiant_id)
            passage = Passage(etudiant=etudiant)
            passage.full_clean()  # Valide les contraintes
            passage.save()
            self.message_user(request, f"✅ Passage ajouté pour {etudiant}.", messages.SUCCESS)
        except Etudiant.DoesNotExist:
            self.message_user(request, "❌ Étudiant introuvable.", messages.ERROR)
        except ValidationError as e:
            # Récupère le message d’erreur propre
            message = e.messages[0] if e.messages else "Erreur de validation."
            self.message_user(request, f"⚠️ {message}", messages.ERROR)

        return redirect('/admin/inscription/etudiant/')
    def ajouter_passage_bouton(self, obj):
        return format_html(
            '<a class="button" href="{}">Ajouter passage</a>',
            f'/admin/inscription/etudiant/{obj.id}/ajouter_passage/'
        )

    ajouter_passage_bouton.short_description = "Passage"
    ajouter_passage_bouton.allow_tags = True



@admin.register(AnneeScolaire)
class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'active')

@admin.register(Symbole)
class SymboleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'icone')

@admin.register(Passage)  # ✅ C'est le décorateur
class PassageAdmin(admin.ModelAdmin):
    list_display = ('etudiant_nom', 'carte_etudiant', 'date_naissance','etudiant__symbole', 'date_passage')
    search_fields = ('etudiant__nom', 'etudiant__prenom', 'etudiant__carte_etudiant','date_naissance')
    list_filter = ('date_passage', 'etudiant__annee_scolaire', 'etudiant__symbole')


    def etudiant_nom(self, obj):
        return f"{obj.etudiant.prenom} {obj.etudiant.nom}"

    etudiant_nom.short_description = "Étudiant"

    def carte_etudiant(self, obj):
        return obj.etudiant.carte_etudiant

        carte_etudiant.short_description = "Carte étudiant"

    def date_naissance(self, obj):
        return obj.etudiant.date_naissance.strftime('%d/%m/%Y')

    date_naissance.short_description = "Date de naissance"