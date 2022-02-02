from django import forms


class GuestUploadFileForm(forms.Form):
    file = forms.FileField()


class UserUploadFileForm(forms.Form):
    file = forms.FileField()
    private = forms.BooleanField(required=False)
