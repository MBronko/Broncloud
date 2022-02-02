from django.db import models

from django.conf import settings
import uuid
import os


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join(settings.MEDIA_ROOT, filename)


class Url(models.Model):
    url = models.TextField()


class File(models.Model):
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)
    filename = models.TextField(default='unknown')


class IdBinding(models.Model):
    binding_id = models.CharField(max_length=10)
    url = models.ForeignKey(Url, on_delete=models.CASCADE, blank=True, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.binding_id
