from django import forms
from .models import Etudiant

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom', 'prenom', 'date_naissance', 'telephone', 'carte_etudiant', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre prénom'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 0612345678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@email.com'}),
            'carte_etudiant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ETU123456'}),        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionnel : accepter les deux formats
        self.fields['date_naissance'].input_formats = ['%Y-%m-%d']