from django import forms

from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['surname', 'name', 'patronymic','position_at_work']


class ImageForm(forms.Form):
    user_id = forms.IntegerField(required=True)
    image = forms.ImageField(required=True)


class UpdateUserForm(forms.Form):
    user_id = forms.IntegerField(required=True)
    surname = forms.CharField(required=False)
    name = forms.CharField(required=False)
    patronymic = forms.CharField(required=False)
    position_at_work = forms.CharField(required=False)


class ResultForm(forms.Form):
    user_id = forms.IntegerField()
    image_id = forms.IntegerField()

    structure_asymmetry = forms.BooleanField(required=False)
    blue_white_structures = forms.BooleanField(required=False)
    atypical_pigment_network = forms.BooleanField(required=False)
    radial_radiance = forms.BooleanField(required=False)
    points = forms.BooleanField(required=False)
    diagnosis = forms.CharField(required=False)


class UpdateResultForm(forms.Form):
    result_id = forms.IntegerField()
    user_id = forms.IntegerField(required=True)

    structure_asymmetry = forms.BooleanField(required=False)
    blue_white_structures = forms.BooleanField(required=False)
    atypical_pigment_network = forms.BooleanField(required=False)
    radial_radiance = forms.BooleanField(required=False)
    points = forms.BooleanField(required=False)
    diagnosis = forms.CharField(required=False)


class DownloadImageForm(forms.Form):
    image_id = forms.IntegerField()

