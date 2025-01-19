from django.urls import path
from utilisateurs import views
urlpatterns = [
    path('', views.index, name='index'),
    path('inscription/eleve/', views.inscription_eleve, name='inscription_eleve'),
    path('inscription/enseignant/', views.inscription_enseignant, name='inscription_enseignant'),
    path('user_login/', views.user_login, name='user_login'),
    path('update_profile/', views.update_profile, name='update_profile'),  # Correction ici
    path('home/', views.home, name='home'),
    path('play_message/', views.play_message, name='play_message'),
    path('user_logout/', views.user_logout, name='user_logout'),
]