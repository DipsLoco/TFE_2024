from django.contrib import admin
from .models import User, Workout, Booking, Coach, Location, Plan, Subscription, Review

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'role', 'last_name', 'first_name', 'birth_date', 'email', 'phone', 'address', 'postal_code', 'is_premium', 'social_url']


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'duration', 'available', 'created_at', 'image']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'workout', 'datetime', 'available', 'location']
    filter_horizontal = ['participants']

class CoachAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'user', 'available']
    filter_horizontal = ['specialties']

class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'city', 'state', 'postal_code']

class PlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'duration']

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'plan', 'start_date', 'payment_status']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'workout', 'content']

admin.site.register(User, UserAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Coach, CoachAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Review, ReviewAdmin)
