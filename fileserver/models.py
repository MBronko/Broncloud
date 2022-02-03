from django.db import models

from django.conf import settings
import uuid
import os


# def get_file_path(instance, filename):
#     print('asd', filename)
#     ext = filename.split('.')[-1]
#     filename = f'{uuid.uuid4()}.{ext}'
#     return os.path.join(settings.MEDIA_ROOT, filename)


class Url(models.Model):
    redirect_url = models.TextField()

    def __str__(self):
        return self.redirect_url


class File(models.Model):
    file = models.FileField(upload_to='', blank=True, null=True)
    filename = models.TextField(default='unknown')

    def __str__(self):
        return self.filename


class IdBinding(models.Model):
    binding_id = models.CharField(max_length=10)
    url = models.ForeignKey(Url, on_delete=models.CASCADE, blank=True, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.binding_id
