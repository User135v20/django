from django import forms
from .models import Patient

# первый варик
#class PatientForm(forms.Form):
    # surname = forms.CharField(max_length=50)
    # name = forms.CharField(max_length=50)
    # patronymic = forms.CharField(max_length=50)


# второй варик
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['surname', 'name', 'patronymic']