from django.shortcuts import render
from .forms import GuestUploadFileForm, UserUploadFileForm
from django.http import HttpResponse, FileResponse
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .tools import *
from .models import File, IdBinding


@method_decorator(csrf_exempt, name='dispatch')
class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = UserUploadFileForm()
        else:
            form = GuestUploadFileForm()

        context = {
            'form': form
        }

        return render(request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = UserUploadFileForm(request.POST, request.FILES)
        else:
            form = GuestUploadFileForm(request.POST, request.FILES)

        print(request.POST, request.FILES, form.is_valid())

        if form.is_valid():
            # file = handle_file(request.FILES['file'])
            uploaded_file = request.FILES['file']

            file = File(file=uploaded_file, filename=uploaded_file.name)
            file.save()

            binding_id = random_binding_id()

            IdBinding(file=file, binding_id=binding_id).save()

            return HttpResponse(f'{request.get_host()}/{binding_id}')

        return HttpResponse('Invalid form data')


def get_resource(request, resource_id):
    resource_id = resource_id.split('.')[0]
    try:
        binding = IdBinding.objects.get(binding_id=resource_id)
        file = binding.file
        filename = file.filename

        return FileResponse(file.file, filename=filename)

    except IdBinding.DoesNotExist as e:
        return HttpResponse('Invalid resource id')
