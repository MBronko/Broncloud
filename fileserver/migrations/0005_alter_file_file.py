# Generated by Django 4.0.2 on 2022-02-02 19:33

from django.db import migrations, models
import fileserver.models


class Migration(migrations.Migration):

    dependencies = [
        ('fileserver', '0004_remove_file_ext_remove_file_filename_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=fileserver.models.get_file_path),
        ),
    ]