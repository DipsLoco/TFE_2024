# Generated by Django 4.2.1 on 2024-07-22 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0014_delete_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='plan_images/'),
        ),
    ]
