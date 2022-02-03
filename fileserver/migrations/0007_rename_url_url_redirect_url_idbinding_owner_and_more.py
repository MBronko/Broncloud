# Generated by Django 4.0.2 on 2022-02-03 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fileserver', '0006_file_filename'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='url',
            new_name='redirect_url',
        ),
        migrations.AddField(
            model_name='idbinding',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idbinding',
            name='private',
            field=models.BooleanField(default=False),
        ),
    ]