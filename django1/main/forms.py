from django import forms

from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['surname', 'name', 'patronymic']


class UpdatePatientForm(forms.Form):
    patient_id = forms.IntegerField(required=True)
    surname = forms.CharField(required=False)
    name = forms.CharField(required=False)
    patronymic = forms.CharField(required=False)


class ResultForm(forms.Form):
    patient_id = forms.IntegerField()

    blast_cell = forms.FloatField()
    promyelocytes = forms.FloatField()
    neutrophils_myelocytes = forms.FloatField()
    neutrphils_metamyelocytes = forms.FloatField()
