from django import forms

from .models import Patient
from .models import Image


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['surname', 'name', 'patronymic','position_at_work']

class ImageForm(forms.ModelForm):
    image = forms.ImageField()




class UpdatePatientForm(forms.Form):
    patient_id = forms.IntegerField(required=True)
    surname = forms.CharField(required=False)
    name = forms.CharField(required=False)
    patronymic = forms.CharField(required=False)
    position_at_work = forms.CharField(required=False)



class ResultForm(forms.Form):
    patient_id = forms.IntegerField()
    image_id = forms.IntegerField()

    structure_asymmetry = forms.BooleanField(required=False)
    blue_white_structures = forms.BooleanField(required=False)
    atypical_pigment_network = forms.BooleanField(required=False)
    radial_radiance = forms.BooleanField(required=False)
    points = forms.BooleanField(required=False)


class UpdateResultForm(forms.Form):
    id = forms.IntegerField()
    patient_id = forms.IntegerField(required=False)

    structure_asymmetry = forms.BooleanField(required=True)
    blue_white_structures = forms.BooleanField(required=True)
    atypical_pigment_network = forms.BooleanField(required=True)
    radial_radiance = forms.BooleanField(required=True)
    points = forms.BooleanField(required=True)


