# Generated by Django 4.0.2 on 2022-02-02 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fileserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='filename',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='file',
            name='sha',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='idbinding',
            name='file_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fileserver.file'),
        ),
        migrations.AlterField(
            model_name='idbinding',
            name='url_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fileserver.url'),
        ),
    ]
