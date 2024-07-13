from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
        ('coach', 'Coach'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')  # Rôle de l'utilisateur
    last_name = models.CharField(max_length=100)  # Nom de famille de l'utilisateur
    first_name = models.CharField(max_length=100)  # Prénom de l'utilisateur
    birth_date = models.DateField(default=timezone.now)  # Date de naissance
    email = models.EmailField()  # Adresse email
    phone = models.CharField(max_length=15)  # Numéro de téléphone
    address = models.CharField(max_length=255)  # Adresse postale
    postal_code = models.IntegerField(default=1000)  # Code postal
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
    # password = models.CharField(max_length=128, default='default_password')


class Workout(models.Model):
    title = models.CharField(max_length=200)  # Title of the workout
    description = models.TextField()  # Description of the workout
    duration = models.DurationField()  # Duration of the workout
    available = models.BooleanField(default=True)  # Availability of the workout
    created_at = models.DateTimeField(auto_now_add=True)  # Creation date
    image = models.ImageField(upload_to='workout_images/', blank=True, null=True)  # Image de la séance

    def __str__(self):
        return self.title

class Location(models.Model):
    name = models.CharField(max_length=100)  # Name of the location
    address = models.CharField(max_length=255)  # Address
    city = models.CharField(max_length=100)  # City
    state = models.BooleanField()  # State (whether the location is active or not)
    postal_code = models.IntegerField()  # Postal code

    def __str__(self):
        return self.name

class Booking(models.Model):
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE)  # ID d'un workout
    participants = models.ManyToManyField('User', related_name='bookings')  # Participants
    coach = models.ForeignKey('User', on_delete=models.CASCADE, related_name='coached_bookings')  # ID d'un coach
    location = models.ForeignKey('Location', on_delete=models.CASCADE)  # ID d'une location
    datetime = models.DateTimeField()  # Date et heure de la réservation
    available = models.BooleanField(default=True)  # Disponibilité de la réservation
    expired = models.BooleanField(default=False)  # Expiré par défaut à False

    def update_expired_status(self):
        if self.datetime < timezone.now():
            self.expired = True
            self.save()

# Signal pour mettre à jour le champ 'expired' après chaque sauvegarde de Booking
@receiver(post_save, sender=Booking)
def check_expired_status(sender, instance, **kwargs):
    instance.update_expired_status()

    def clean(self):
        if self.participants.count() > 10:
            raise ValidationError('Vous ne pouvez pas ajouter plus de 10 participants à une réservation.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

def validate_participant_limit(sender, **kwargs):
    if kwargs['instance'].participants.count() > 10:
        raise ValidationError('Vous ne pouvez pas ajouter plus de 10 participants à une réservation.')

m2m_changed.connect(validate_participant_limit, sender=Booking.participants.through)

class Coach(models.Model):
    username = models.CharField(max_length=50, unique=True)  # Username of the coach
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # User ID
    specialties = models.ManyToManyField(Workout, related_name='specialties')  # Coach's specialties
    available = models.BooleanField(default=False)  # Coach's availability

class Plan(models.Model):
    name = models.CharField(max_length=100)  # Name of the plan
    description = models.TextField()  # Description of the plan
    price = models.IntegerField()  # Price of the plan
    duration = models.IntegerField()  # Duration of the plan in days
    image = models.ImageField(upload_to='plan_images/', blank=True, null=True)  # Image du plan
    is_available = models.BooleanField(default=False) # Plan availability

    def __str__(self):
        return self.name

class Subscription(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En Attente'),
        ('paid', 'En ordre de paiement'),
        ('refused', 'Paiement Refusé'),
    ]
    
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # ID de l'utilisateur
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)  # ID du plan
    start_date = models.DateField()  # Date de début de l'abonnement
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )  # Statut du paiement

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User ID
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)  # Workout ID
    content = models.TextField()  # Review content
    datetime = models.DateTimeField()  # Date et heure du commentairecontent = models.TextField()  # Contenu du commentaire
    datetime = models.DateTimeField(default=timezone.now)  # Date et heure du commentaire

