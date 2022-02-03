from django.conf import settings
from django.test import TestCase
from django.http import HttpResponseRedirect, HttpResponse
import os


class FileUploadCase(TestCase):
    def setUp(self):
        self.file = open(os.path.join(settings.BASE_DIR, 'README.md'), 'rb')
        self.credentials = {
            'username': 'testuser',
            'password': 'pasdqqwe121'
        }

    def test_everything(self):
        username = self.credentials['username']
        passwd = self.credentials['password']

        self.client.post('/account/signup/', {'username': username, 'password1': passwd, 'password2': passwd}, follow=True)

        response = self.client.post('/account/login/', self.credentials, follow=True)

        self.assert_(response.context['user'].is_authenticated)  # check if user logged in

        resp = self.client.post('/', {'file': self.file})

        resp_content = str(resp.content, 'UTF-8').split('/')

        self.assert_(resp_content[0] == 'testserver')
        self.assert_(bool(resp_content[-1]))   # check if endpoint returned resource id

        id_ = resp_content[-1]

        saved_filepath = os.path.join(settings.MEDIA_ROOT, id_ + '.md')
        self.assert_(os.path.isfile(saved_filepath))  # check if file is created

        self.file.seek(0)
        actual_file_content = self.file.read()

        resp = self.client.get(f'/{id_}')
        downloaded_file_content = b''.join(resp.streaming_content)

        self.assert_(actual_file_content == downloaded_file_content)  # check if original and downladed file are same

        resp = self.client.post(f'/delete/{id_}')
        self.assert_(isinstance(resp, HttpResponseRedirect))

        resp = self.client.get(f'/{id_}')
        self.assert_(isinstance(resp, HttpResponse))  # check if resource is no longer available

        self.assert_(not os.path.isfile(saved_filepath))  # check if file stored in media directory is still there
