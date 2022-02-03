from django import forms


class GuestUploadFileForm(forms.Form):
    file = forms.FileField()


class UserUploadFileForm(forms.Form):
    file = forms.FileField()
    private = forms.BooleanField(required=False)


class GuestShortenUrlForm(forms.Form):
    url = forms.URLField()


class UserShortenUrlForm(forms.Form):
    url = forms.URLField()
    private = forms.BooleanField(required=False)
