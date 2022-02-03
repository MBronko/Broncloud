from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse, FileResponse
from django.views.generic import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .tools import *
from .models import File, IdBinding, Url


@method_decorator(csrf_exempt, name='dispatch')
class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            file_form = UserUploadFileForm()
            url_form = UserShortenUrlForm
        else:
            file_form = GuestUploadFileForm()
            url_form = GuestShortenUrlForm

        context = {
            'file_form': file_form,
            'url_form': url_form,
        }

        return render(request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = UserUploadFileForm(request.POST, request.FILES)
        else:
            form = GuestUploadFileForm(request.POST, request.FILES)

        print(request.POST, request.FILES, form.is_valid())

        if not form.is_valid():
            return HttpResponse('Invalid form data')

        binding_id = random_binding_id()
        uploaded_file = request.FILES['file']

        old_filename = uploaded_file.name
        ext = old_filename.split('.')[-1]
        uploaded_file.name = f'{binding_id}.{ext}'

        file = File(file=uploaded_file, filename=old_filename)
        file.save()

        if request.user.is_authenticated:
            IdBinding(file=file, binding_id=binding_id, owner=request.user).save()
        else:
            IdBinding(file=file, binding_id=binding_id).save()

        return HttpResponse(f'{request.get_host()}/{binding_id}')


def get_resource(request, resource_id):
    resource_id = resource_id.split('.')[0]
    try:
        binding = IdBinding.objects.get(binding_id=resource_id)

        if binding.file:
            file = binding.file
            filename = file.filename

            return FileResponse(file.file, filename=filename)
        elif binding.url:
            url = binding.url.redirect_url

            return redirect(url)

        return HttpResponse('Id doesnt bind anything. This should not happen')

    except IdBinding.DoesNotExist as e:
        return HttpResponse('Invalid resource id')


@csrf_exempt
def shorten_url(request):
    if request.method != "POST":
        return HttpResponse('Invalid request method')

    if request.user.is_authenticated:
        form = UserShortenUrlForm(request.POST)
    else:
        form = GuestShortenUrlForm(request.POST)

    if not form.is_valid():
        return HttpResponse('Invalid form data')

    url = Url(url=request.POST['url'])
    url.save()

    binding_id = random_binding_id()
    IdBinding(url=url, binding_id=binding_id).save()

    return HttpResponse(f'{request.get_host()}/{binding_id}')
