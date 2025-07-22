from django.contrib import admin
from django.urls import path
from inscription.views import inscription_etudiant, accueil

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accueil, name='accueil'),
    path('inscription/', inscription_etudiant, name='inscription'),
]
