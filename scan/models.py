from django.db import models
from django.urls import reverse
import qrcode
import os
from django.core.files import File
from django.conf import settings
from .utils import generateQrCode
from django.contrib.auth.models import User

class Etudiant(models.Model):
    nom = models.CharField(max_length=100, null=True)
    prenom = models.CharField(max_length=100, null=True)
    telephone = models.CharField(max_length=20)
    adresse_mail = models.EmailField(max_length=100, null=True)
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', null=True)  
    image = models.ImageField(upload_to='etudiant_images/', null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} {self.username}"

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr_code_data = {
                'nom': self.nom,
                'prenom': self.prenom,
                'telephone': self.telephone,
                'adresse_mail': self.adresse_mail,
                'username': self.username
            }
            qr_code_path = generateQrCode(qr_code_data)
            self.qr_code.save(os.path.basename(qr_code_path), File(open(qr_code_path, 'rb')))
        super().save(*args, **kwargs)




class PointageEtudiant(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    date_pointage = models.DateField(auto_now_add=True)
    heure_pointage = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"Pointage de {self.etudiant.nom} {self.etudiant.prenom} - {self.date_pointage} {self.heure_pointage}"
