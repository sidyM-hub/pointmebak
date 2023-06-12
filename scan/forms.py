from django import forms
from .models import Etudiant
from django.contrib.auth.models import User 



class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom', 'prenom', 'telephone', 'adresse_mail','image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'required': False}),
        }


from django import forms

class PointageForm(forms.Form):
    date_debut = forms.DateField(label='Date de début', widget=forms.DateInput(attrs={'type': 'date'}))
    date_fin = forms.DateField(label='Date de fin', widget=forms.DateInput(attrs={'type': 'date'}))
    heure_debut = forms.TimeField(label='Heure de début', widget=forms.TimeInput(attrs={'type': 'time'}))
    heure_fin = forms.TimeField(label='Heure de fin', widget=forms.TimeInput(attrs={'type': 'time'}))





    
       
        
      