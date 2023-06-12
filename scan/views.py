from django.shortcuts import render
import cv2
import numpy as np
import qrcode
from django.contrib.staticfiles.storage import staticfiles_storage
from pyzbar.pyzbar import decode
from scan.models import Etudiant
from .forms import EtudiantForm
# from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib import messages
qr_image = None
from django.shortcuts import render,redirect
#from . import settings
from qrcode import QRCode
from django.core.files.base import ContentFile
from django.core.files import File
from PIL import Image, ImageDraw
from django.db import models
import base64
import os
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseNotFound
from django.http import FileResponse


def accueil(request):
    etudiants = Etudiant.objects.all()
   
    return render(request, "scan/accueil.html",{'etudiants':etudiants}) 

def base(request):
    etudiants = Etudiant.objects.all()
   
    return render(request, "scan/base.html",{'etudiants':etudiants})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Etudiant
from .forms import EtudiantForm
from django.conf import settings
import qrcode


# def generateQrCode(data):
#     qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
#     full_name = f"{data['nom']} {data['prenom']} ({data['telephone']}, {data['adresse_mail']})"
#     qr.add_data(full_name)
#     qr.make(fit=True)
#     img = qr.make_image(fill_color="black", back_color="white")
#     img_file = f"{settings.MEDIA_ROOT}/qr_codes/{data['username']}.png"
#     img.save(img_file)
#     return img_file


def generateQrCode(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    full_name = f"{data['nom']} {data['prenom']} ({data['telephone']}, {data['adresse_mail']})"
    qr.add_data(full_name)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_file = f"{settings.MEDIA_ROOT}/qr_codes/{data['username']}.png"
    img.save(img_file)
    return img_file

from django.shortcuts import render, redirect
from .models import Etudiant
from .forms import EtudiantForm

from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.shortcuts import render, redirect
from .models import Etudiant
from .forms import EtudiantForm
from .utils import generateQrCode
from django.contrib import messages
import os
from django.core.files import File
from django.conf import settings


def ListeEtudiants(request):
    etudiants = Etudiant.objects.all()
    return render(request, 'scan/ListeEtudiants.html', {'etudiants': etudiants})



def ajout(request):
    etudiants = Etudiant.objects.all()
    
    if request.method == "POST":
        form = EtudiantForm(request.POST)
        
        if form.is_valid():
            etudiant = form.save(commit=False)
            etudiant.save()

            if 'image' in request.FILES:
                etudiant.image = request.FILES['image']
                etudiant.save()

            qr_code_data = {
                'nom': etudiant.nom,
                'prenom': etudiant.prenom,
                'telephone': etudiant.telephone,
                'adresse_mail': etudiant.adresse_mail,
                'username': etudiant.username
            }
            
            qr_code_path = generateQrCode(qr_code_data)
            etudiant.qr_code.save(os.path.basename(qr_code_path), File(open(qr_code_path, 'rb')))
            etudiant.save()

            messages.success(request, "L'étudiant a été créé avec succès !")
            return redirect('accueil')
        else:
            messages.error(request, "Erreur lors de la création de l'étudiant. Veuillez vérifier les informations.")
    else:
        form = EtudiantForm()
        etudiants = Etudiant.objects.all()

    return render(request, "scan/ajout.html", {'form': form, 'etudiants': etudiants})




import cv2
from pyzbar import pyzbar

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse




from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import qrcode



import json


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required




import cv2
import pyzbar.pyzbar as pyzbar
from pyzbar.pyzbar import ZBarSymbol
from .models import Etudiant
# views.py
from django.shortcuts import render
from django.http import JsonResponse

from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from django.http import JsonResponse
from .models import Etudiant, PointageEtudiant

def scanner(request):
    return render(request, 'scan/scanner.html')

def verifier_qr_code(request):
    if request.method == 'POST':
        qr_code = request.POST.get('qr_code')
        
        try:
            etudiant = Etudiant.objects.get(qr_code=qr_code)
            now = datetime.now()
            
            # Enregistrer le pointage de l'étudiant
            pointage = PointageEtudiant.objects.create(
                etudiant=etudiant,
                date_pointage=now.date(),
                heure_pointage=now.time()
            )
            
            response_data = {
                'valide': True,
                'pointages': list(PointageEtudiant.objects.values('etudiant__telephone', 'date_pointage', 'heure_pointage')),
            }
            return JsonResponse(response_data)
        except Etudiant.DoesNotExist:
            return JsonResponse({'valide': False, 'erreur': 'QR code non valide'})

    return JsonResponse({'valide': False, 'erreur': 'Méthode non autorisée'})

def liste(request):
    pointages = PointageEtudiant.objects.all().values('etudiant__telephone', 'date_pointage', 'heure_pointage')
    return render(request, 'scan/liste.html', {'pointages': pointages})









from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .models import Etudiant
from .forms import EtudiantForm

# ...
from django.core.mail import EmailMessage
from email.mime.image import MIMEImage

# views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import EtudiantForm

from django.shortcuts import get_object_or_404

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from .forms import EtudiantForm

def envoi(request):
    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES)
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            prenom = form.cleaned_data.get('prenom')
            telephone = form.cleaned_data.get('telephone')
            adresse_mail = form.cleaned_data.get('adresse_mail')
            image = form.cleaned_data.get('image')

            # Vérifier si l'étudiant existe déjà dans la base de données
            etudiant = Etudiant.objects.filter(nom=nom, prenom=prenom, telephone=telephone).first()

            # Si l'étudiant existe, envoyer l'e-mail
            if etudiant:
                # Envoyer l'e-mail
                message = f"Bienvenue à notre université !\n\n" \
                          f"Merci d'avoir rejoint notre université. Voici vos informations :\n" \
                          f"Nom: {nom}\n" \
                          f"Prénom: {prenom}\n" \
                          f"Téléphone: {telephone}\n" \
                          f"Adresse e-mail: {adresse_mail}\n"

                email = EmailMessage(
                    'Bienvenue à notre université !',
                    message,
                    'scbakeli@gmail.com',
                    [adresse_mail],
                )

                email.attach(image.name, image.read(), image.content_type)
                email.send()

            return redirect('accueil')
    else:
        form = EtudiantForm()
    return render(request, 'scan/envoi.html', {'form': form})




from django.shortcuts import render
from django.http import HttpResponse

def details_etudiant(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Rechercher l'étudiant en utilisant l'adresse e-mail
        etudiant = Etudiant.objects.filter(adresse_mail=email).first()

        if etudiant:
            return render(request, 'scan/details_etudiant.html', {'etudiant': etudiant})
        else:
            # Étudiant non trouvé, renvoyer à la page "etudiant_non_trouve.html"
            return render(request, 'scan/etudiant_non_trouve.html')

    # Requête GET, afficher le formulaire de recherche vide
    return render(request, 'scan/details_etudiant.html')





def etudiant_non_trouve(request):
    return render(request, 'scan/etudiant_non_trouve.html')