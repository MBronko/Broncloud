import rstr
from .models import IdBinding


def random_binding_id():
    length = 4

    while True:
        binding_id = rstr.xeger('[A-Za-z]{%s}' % length)

        try:
            IdBinding.objects.get(binding_id=binding_id)
        except IdBinding.DoesNotExist:
            break

    return binding_id


def get_resource_url(request, binding_id):
    return f'{request.get_host()}/{binding_id}'
