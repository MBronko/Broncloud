# Generated by Django 4.0.2 on 2022-02-02 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileserver', '0005_alter_file_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='filename',
            field=models.TextField(default='unknown'),
        ),
    ]
