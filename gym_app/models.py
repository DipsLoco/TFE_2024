from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_save
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
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
    date_joined = models.DateTimeField(default=timezone.now)  # Date de création du compte
    social_url = models.URLField(blank=True, null=True)  # URL des réseaux sociaux
    image = models.ImageField(upload_to='membre_images/', blank=True, null=True)  # Image du membre
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)  # Nom unique pour éviter les conflits
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)  # Nom unique pour éviter les conflits


class Location(models.Model):
    name = models.CharField(max_length=100)  # Nom de la location
    address = models.CharField(max_length=255)  # Adresse
    city = models.CharField(max_length=100)  # Ville
    state = models.BooleanField()  # Statut (location active ou non ?)
    postal_code = models.IntegerField()  # Code postal

    def __str__(self):
        return self.name


class Workout(models.Model):
    title = models.CharField(max_length=200)  # Titre de la séance
    description = models.TextField()  # Description de la séance
    duration = models.DurationField()  # Durée de la séance
    available = models.BooleanField(default=True)  # Disponibilité de la séance
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # Localisation de la séance
    coachs = models.ManyToManyField('Coach', related_name='workouts')  # Coachs associés à la séance

    def __str__(self):
        return self.title

    def get_main_image(self):
        return self.images.first()  # Retourne la première image associée à ce Workout


class WorkoutImage(models.Model):
    workout = models.ForeignKey(Workout, related_name='images', on_delete=models.CASCADE)  # Séance associée
    image = models.ImageField(upload_to='workout_images/')  # Image de la séance
    description = models.CharField(max_length=255, blank=True, null=True)  # Description de l'image

    def __str__(self):
        return self.description if self.description else f'Image for {self.workout.title}'


class Booking(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)  # ID d'un workout
    participants = models.ManyToManyField(User, related_name='bookings')  # Participants
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coached_bookings')  # ID d'un coach
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # ID d'une location
    datetime = models.DateTimeField()  # Date et heure de la réservation
    available = models.BooleanField(default=True)  # Disponibilité de la réservation
    expired = models.BooleanField(default=False)  # Expiré par défaut à False

    def update_expired_status(self):
        if self.datetime < timezone.now():
            self.expired = True
            self.save()

    # Signal pour mettre à jour le champ 'expired' après chaque sauvegarde de Booking
    @receiver(post_save, sender='gym_app.Booking') 
    def check_expired_status(sender, instance, **kwargs):
        instance.update_expired_status()

    def clean(self):
        if self.participants.count() > 10:
            raise ValidationError('Vous ne pouvez pas ajouter plus de 10 participants à une réservation.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# Fonction pour valider le nombre de participants
def validate_participant_limit(sender, **kwargs):
    if kwargs['instance'].participants.count() > 10:
        raise ValidationError('Vous ne pouvez pas ajouter plus de 10 participants à une réservation.')


m2m_changed.connect(validate_participant_limit, sender=Booking.participants.through)


class Coach(models.Model):
    username = models.CharField(max_length=50, unique=True)  # Nom d'utilisateur du coach
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ID de l'utilisateur
    specialties = models.ManyToManyField(Workout, related_name='specialties')  # Spécialités du coach
    available = models.BooleanField(default=False)  # Disponibilités du coach
    image = models.ImageField(upload_to='coach_images/', blank=True, null=True)  # Image du coach
    exp = models.PositiveIntegerField(default=0)  # Expérience du coach en années

    def __str__(self):
        return self.username


class Plan(models.Model):
    name = models.CharField(max_length=100)  # Nom du plan
    description = models.TextField()  # Description du plan
    price = models.IntegerField()  # Prix du plan
    duration = models.IntegerField()  # Durée du plan en jours
    image = models.ImageField(upload_to='plan_images/', blank=True, null=True)  # Image du plan
    is_available = models.BooleanField(default=False)  # Disponibilité du plan

    def __str__(self):
        return self.name


class Subscription(models.Model):  # Statut abonnement
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('paid', 'En ordre de paiement'),
        ('refused', 'Paiement refusé'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ID de l'utilisateur
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)  # ID du plan
    start_date = models.DateField(auto_now_add=True)  # Date de début de l'abonnement
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')  # Statut du paiement


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ID de l'utilisateur
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)  # ID de la séance
    content = models.TextField()  # Contenu du commentaire utilisateur
    datetime = models.DateTimeField(default=timezone.now)  # Date et heure du commentaire
