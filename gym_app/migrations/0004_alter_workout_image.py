# Generated by Django 4.2.1 on 2024-07-12 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0003_booking_expired_plan_is_available_review_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='workout_images/'),
        ),
    ]