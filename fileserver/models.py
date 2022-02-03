from django.db import models

from django.conf import settings
from django.dispatch import receiver
import os


class Url(models.Model):
    """
    Model used to store URLs that URL shortener redirects to
    """
    redirect_url = models.TextField()

    def __str__(self):
        return self.redirect_url


class File(models.Model):
    """
    Model used to store informaction about files stored in media directory
    """
    file = models.FileField(blank=True, null=True)
    filename = models.TextField(default='unknown')

    def __str__(self):
        return self.filename


class IdBinding(models.Model):
    """
    Model used to store information about resource stored in either Url or File model
    """
    binding_id = models.CharField(max_length=10)
    url = models.ForeignKey(Url, on_delete=models.CASCADE, blank=True, null=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.binding_id


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `File` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.post_delete, sender=IdBinding)
def handle_deleted_idbinding(sender, instance, **kwargs):
    """
    Deletes file and url objects corresponding to the removed IdBinding object
    """
    if instance.file:
        instance.file.delete()
    if instance.url:
        instance.file.delete()
