# Generated by Django 4.2.1 on 2024-07-24 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0018_alter_user_date_joined'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='coachs',
            field=models.ManyToManyField(related_name='workouts', to='gym_app.coach'),
        ),
        migrations.AddField(
            model_name='workout',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gym_app.location'),
            preserve_default=False,
        ),
    ]
