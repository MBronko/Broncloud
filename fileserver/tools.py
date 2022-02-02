import hashlib
import rstr
from .models import IdBinding
from django.conf import settings


def random_binding_id():
    length = 4

    while True:
        binding_id = rstr.xeger('[A-Z]{%s}' % length)

        try:
            IdBinding.objects.get(binding_id=binding_id)
        except IdBinding.DoesNotExist:
            break

    return binding_id
