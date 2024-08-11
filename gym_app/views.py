from django.shortcuts import get_object_or_404, redirect, render
from gym_app.models import Booking, Coach, Plan, Review, Workout, WorkoutImage
from django.shortcuts import get_object_or_404, redirect, render
from gym_app.models import Booking, Coach, Plan, Review, Workout, WorkoutImage
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from gym_app.models import Booking, Coach, Plan, Review, Workout, WorkoutImage


User = get_user_model()

# Vue pour la page à propos
def about(request):
    return render(request, 'about.html')

# Vue pour la page d'accueil
def home(request):
    plans = Plan.objects.filter(is_available=True)
    workouts = Workout.objects.filter(available=True)
    coachs = Coach.objects.all()
    reviews = Review.objects.all()
    bookings = Booking.objects.select_related('coach', 'location').all()
    return render(request, 'home.html', {'plans': plans, 'workouts': workouts, 'coachs': coachs, 'reviews': reviews, 'bookings': bookings})

# Vue pour la page faq
def faq(request):
    return render(request, 'faq.html')

# Vue pour la page Abonnement
def plan(request, pk):
    plan = Plan.objects.get(id=pk)
    return render(request, 'plan.html', {'plan': plan})

# Vue pour la page d'accueil
def home(request):
    plans = Plan.objects.filter(is_available=True)
    workouts = Workout.objects.filter(available=True)
    coachs = Coach.objects.all()
    reviews = Review.objects.all()
    bookings = Booking.objects.select_related('coach', 'location').all()
    return render(request, 'home.html', {'plans': plans, 'workouts': workouts, 'coachs': coachs, 'reviews': reviews, 'bookings': bookings})

# Vue pour la page faq
def faq(request):
    return render(request, 'faq.html')

# Vue pour la page Abonnement
def plan(request, pk):
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
            messages.success(request, f'Bienvenue, {user.username}!')
            messages.success(request, f'Bienvenue, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
            return render(request, 'administration/login.html')
    else:        
        return render(request, 'administration/login.html')
    
# Vue pour la déconnexion utilisateur
def logout_user(request):
    user = request.user
    user = request.user
    logout(request)
    messages.success(request, f'Aurevoir et à bientôt, {user.username}!')
    messages.success(request, f'Aurevoir et à bientôt, {user.username}!')
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
                messages.success(request, f'Vous êtes maintenant inscrit, {user.username}!')
                messages.success(request, f'Vous êtes maintenant inscrit, {user.username}!')
                return redirect('home')
        else:
            messages.error(request, 'Erreur lors de l\'inscription')
            messages.error(request, 'Erreur lors de l\'inscription')
            return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'administration/register.html', {'form': form})

@receiver(post_save, sender=User)
def create_or_update_coach(sender, instance, created, **kwargs):
    if instance.role == 'coach':
        Coach.objects.update_or_create(
            user=instance,
            defaults={
                'username': instance.username,
                'image': instance.image
            }
        )
    else:
        Coach.objects.filter(user=instance).delete()

def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    images = WorkoutImage.objects.filter(workout=pk)
    return render(request, 'workout.html', {'workout': workout, 'images': images})


