from django.shortcuts import get_object_or_404, redirect, render
from gym_app.models import Coach, Plan, Review, Workout, WorkoutImage, Review
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms




# Vue pour la page à propos
def about(request):
    return render(request, 'about.html')

# Vue pour la page d'accueil
def home(request):
    # Récupère tous les plans disponibles
    plans = Plan.objects.filter(is_available=True)
    # Récupère tous les workouts disponibles
    workouts = Workout.objects.filter(available=True)
    # Récupère tous les coachs
    coachs = Coach.objects.all()
    # Récupère tous les commentaires
    reviews = Review.objects.all()
    return render(request, 'home.html', {'plans': plans, 'workouts': workouts, 'coachs': coachs, 'reviews': reviews,})



# Vue pour la page faq
def faq(request):
    return render(request,'faq.html')

# Vue pour la page Abonnement
def plan(request,pk):
    plan = Plan.objects.get(id=pk)
    return render(request, 'plan.html', {'plan': plan})



# Vue pour la connexion utilisateur
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Vous êtes connecté'))
            return redirect('home')
        else:
            messages.error(request, ('Nom d\'utilisateur ou mot de passe incorrect'))
            return render(request, 'administration/login.html')
    else:        
        return render(request, 'administration/login.html')



# Vue pour la déconnexion utilisateur
def logout_user(request):
    logout(request)
    messages.success(request, ("Vous avez été déconnecté"))
    return redirect('home')

# Vue pour l'inscription d'un nouvel utilisateur
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ('Vous êtes inscrit'))
                return redirect('home')
        else:
            messages.error(request, ('Erreur lors de l\'inscription'))
            return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'administration/register.html', {'form': form})

def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    images = WorkoutImage.objects.filter(workout=pk)
    return render(request, 'workout.html', {'workout': workout, 'images': images})
