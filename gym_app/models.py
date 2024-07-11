from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('coach', 'Coach'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')  # Rôle de l'utilisateur
    last_name = models.CharField(max_length=100)  # Nom de famille de l'utilisateur
    first_name = models.CharField(max_length=100)  # Prénom de l'utilisateur
    birth_date = models.DateField()  # Date de naissance
    email = models.EmailField()  # Adresse email
    phone = models.CharField(max_length=15)  # Numéro de téléphone
    address = models.CharField(max_length=255)  # Adresse postale
    postal_code = models.IntegerField()  # Code postal
    is_premium = models.BooleanField(default=False)  # Statut premium
    social_url = models.URLField(blank=True, null=True)  # URL des réseaux sociaux

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Nom unique pour éviter les conflits
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Nom unique pour éviter les conflits
        blank=True
    )
    
    # Ajouter un mot de passe par défaut
    password = models.CharField(max_length=128, default='default_password')


class Workout(models.Model):
    title = models.CharField(max_length=200)  # Title of the workout
    description = models.TextField()  # Description of the workout
    duration = models.DurationField()  # Duration of the workout
    available = models.BooleanField(default=True)  # Availability of the workout
    created_at = models.DateTimeField(auto_now_add=True)  # Creation date
    image = models.URLField(blank=True, null=True)  # Image URL

class Location(models.Model):
    name = models.CharField(max_length=100)  # Name of the location
    address = models.CharField(max_length=255)  # Address
    city = models.CharField(max_length=100)  # City
    state = models.BooleanField()  # State (whether the location is active or not)
    postal_code = models.IntegerField()  # Postal code

class Booking(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)  # ID of a workout
    participants = models.ManyToManyField(User, related_name='bookings')  # Participants
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coached_bookings')  # ID of a coach
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # ID of a location
    datetime = models.DateTimeField()  # Date and time of the booking
    available = models.BooleanField(default=True)  # Booking availability

    def clean(self):
        if self.participants.count() > 10:
            raise ValidationError('You cannot add more than 10 participants to a booking.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

def validate_participant_limit(sender, **kwargs):
    if kwargs['instance'].participants.count() > 10:
        raise ValidationError('You cannot add more than 10 participants to a booking.')

m2m_changed.connect(validate_participant_limit, sender=Booking.participants.through)

class Coach(models.Model):
    username = models.CharField(max_length=50, unique=True)  # Username of the coach
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # User ID
    specialties = models.ManyToManyField(Workout, related_name='specialties')  # Coach's specialties
    available = models.BooleanField(default=True)  # Coach's availability

class Plan(models.Model):
    name = models.CharField(max_length=100)  # Name of the plan
    description = models.TextField()  # Description of the plan
    price = models.IntegerField()  # Price of the plan
    duration = models.IntegerField()  # Duration of the plan in days

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User ID
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)  # Plan ID
    start_date = models.DateField()  # Start date of the subscription
    payment_status = models.BooleanField(default=False)  # Payment status

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User ID
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)  # Workout ID
    content = models.TextField()  # Review content
