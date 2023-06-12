from django.urls import path
from . import views
from .views import *
from scan.views import accueil, scanner
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from .views import scanner, verifier_qr_code,liste,ListeEtudiants




urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('scanner/', views.scanner, name='scanner'),
    path('verifier_qr_code/', views.verifier_qr_code, name='verifier_qr_code'),
    path('liste/', views.liste, name='liste'),
    path('ajout/', views.ajout, name='ajout'),
    path('ListeEtudiants/', views.ListeEtudiants, name='ListeEtudiants'),
    path('base/', views.base, name='base'),
    path('details_etudiant/', views.details_etudiant, name='details_etudiant'),
    path('etudiant_non_trouve/', views.etudiant_non_trouve, name='etudiant_non_trouve'),
    path('envoi/', views.envoi, name='envoi'),
    
]    