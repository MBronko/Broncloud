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
            file_form = UserUploadFileForm
            url_form = UserShortenUrlForm
            posted_files = IdBinding.objects.filter(owner=request.user, file__isnull=False)
            posted_urls = IdBinding.objects.filter(owner=request.user, url__isnull=False)
        else:
            file_form = GuestUploadFileForm
            url_form = GuestShortenUrlForm
            posted_files = []
            posted_urls = []

        context = {
            'file_form': file_form,
            'url_form': url_form,
            'posted_files': posted_files,
            'posted_urls': posted_urls,
        }

        return render(request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = UserUploadFileForm(request.POST, request.FILES)
            private = request.POST.get('private') == 'on'
        else:
            form = GuestUploadFileForm(request.POST, request.FILES)
            private = False

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
            IdBinding(file=file, binding_id=binding_id, owner=request.user, private=private).save()
        else:
            IdBinding(file=file, binding_id=binding_id).save()

        return HttpResponse(get_resource_url(request, binding_id))


def get_resource(request, resource_id):
    resource_id = resource_id.split('.')[0]
    try:
        binding = IdBinding.objects.get(binding_id=resource_id)

        if binding.private and not request.user.is_superuser and binding.owner != request.user:
            return HttpResponse('Unauthorized access, only for owner')

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
        private = request.POST.get('private') == 'on'
    else:
        form = GuestShortenUrlForm(request.POST)
        private = False

    if not form.is_valid():
        return HttpResponse('Invalid form data')

    url = Url(redirect_url=request.POST['url'])
    url.save()

    binding_id = random_binding_id()

    if request.user.is_authenticated:
        IdBinding(url=url, binding_id=binding_id, owner=request.user, private=private).save()
    else:
        IdBinding(url=url, binding_id=binding_id).save()

    return HttpResponse(get_resource_url(request, binding_id))


def delete_resource(request, resource_id):
    try:
        binding = IdBinding.objects.get(binding_id=resource_id)

        if binding.owner != request.user:
            return HttpResponse('Only owner can remove resource')

        if binding.file:
            binding.file.delete()

        if binding.url:
            binding.url.delete()

        binding.delete()
        return redirect('home')

    except IdBinding.DoesNotExist as e:
        return HttpResponse('Invalid resource id')

