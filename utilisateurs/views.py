from django.shortcuts import render, redirect
from django.contrib import admin
from django.http import HttpResponse , HttpResponseRedirect
from .forms import UserForm, EleveForm, EnseignantForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from utilisateurs.models import Eleve, Enseignant, User
from django.urls import reverse
import json
from .forms import UserForm
import pyttsx3
from django.views.generic import UpdateView

def index(request):
    return render(request, 'index.html')




def inscription_eleve(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        eleve_form = EleveForm(request.POST,request.FILES)
        if user_form.is_valid() and eleve_form.is_valid():
            user = user_form.save()
            user.save()
            eleve = eleve_form.save(commit=False)
            eleve.user = user
            eleve.save()
            return redirect('user_login')  # Redirect to homepage
        else:
            print(user_form.errors, eleve_form.errors)

    else:
        user_form = UserForm()
        eleve_form = EleveForm()
    return render(request, 'inscription_eleve.html',
                  {'user_form': user_form,
                   'eleve_form': eleve_form})

def inscription_enseignant(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        enseignant_form = EnseignantForm(request.POST)
        if user_form.is_valid() and enseignant_form.is_valid():
            user = user_form.save()
            user.save()
            enseignant = enseignant_form.save(commit=False)
            enseignant.user =user
            enseignant.save()
            return redirect('index')  # Redirect to homepage
        else:
            print(user_form.errors, enseignant_form.errors)
    else:
        user_form = UserForm()
        enseignant_form = EnseignantForm()
    return render(request, 'inscription_enseignant.html',
                  {'user_form': user_form,
                   'enseignant_form': enseignant_form})
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect('/admin/')
                elif hasattr(user, 'enseignant') and user.enseignant.first_login:
                    user.enseignant.first_login = False
                    user.enseignant.save()
                    return HttpResponseRedirect('/update_profile/')  # Assurez-vous que cette URL correspond à celle de votre vue de mise à jour de profil
                else:
                    return HttpResponseRedirect('/home/')  # Correction ici
            else:
                return HttpResponse("ACCOUNT IS DEACTIVATED")
        else:
            return HttpResponse("Please use correct id and password")

    else:
        return render(request, 'login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def play_message(user):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    message = f"Bonjour {user.first_name} ! je suis Tweety bott votre assistant virtuelle, si vous avez besoin de mon aide n'hésiter pas de me consulter en bas de la page  a droite "
    engine.setProperty('rate', 145)
    engine.say(message)
    engine.runAndWait()
    engine.stop()
from django.template import loader
import threading

from django.template import loader
from django.contrib.sessions.models import Session
from .models import Eleve

def home(request):
    if request.user.is_authenticated:
        # Vérifier si l'utilisateur est un élève
        if Eleve.objects.filter(user=request.user).exists():
            # Vérifier si le message n'a pas déjà été lu
            if 'message_read' not in request.session:
                # Utilisation d'un thread pour exécuter la tâche de lecture du message en arrière-plan
                threading.Thread(target=play_message, args=(request.user,), daemon=True).start()
                # Marquer le message comme lu en enregistrant une variable de session
                request.session['message_read'] = True

    template = loader.get_template('home.html')
    return HttpResponse(template.render({}, request))

from django.contrib.auth import update_session_auth_hash

@login_required
def update_profile(request):
    user = request.user
    if hasattr(user, 'eleve'):
        profile = user.eleve
        profile_form_class = EleveForm
    elif hasattr(user, 'enseignant'):
        profile = user.enseignant
        profile_form_class = EnseignantForm
    else:
        profile = None
        profile_form_class = None

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = profile_form_class(request.POST, request.FILES, instance=profile) if profile_form_class else None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            update_session_auth_hash(request, user)  # Maintient la session active après la mise à jour
            return redirect('home')  # Redirige vers la page d'accueil après mise à jour
        else:
            print(user_form.errors, profile_form.errors if profile_form else None)
    else:
        user_form = UserForm(instance=user)
        profile_form = profile_form_class(instance=profile) if profile_form_class else None

    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
