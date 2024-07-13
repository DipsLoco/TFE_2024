from django.shortcuts import render

from gym_app.models import Plan, Workout

# Create your views here.
def home(request):
    plans = Plan.objects.filter(is_available=True)
    workouts = Workout.objects.filter(available=True)
    return render(request, 'home.html', {'plans': plans, 'workouts': workouts})
