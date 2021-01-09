from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render
from .forms import PatientForm, UpdatePatientForm
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

# Create your views here.
from .models import Result, Patient


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


def results(request):
    results = Result.objects.all()
    return render(request, 'main/results.html', {'all_results_list': results})


class PatientView:
    @staticmethod
    def list(request):
        results = Patient.objects.all()
        return render(request, 'main/patients.html', {'patients': results})

    @staticmethod
    def delete(request, pk=None):
        patient = Patient.objects.get(id=pk)
        patient.delete()
        patients = Patient.objects.all()
        return render(request, 'main/patients.html', {'patients': patients})

    @staticmethod
    @csrf_protect
    def update(request):
        if request.method == "POST":
            input_patient_data = UpdatePatientForm(request.POST)
            if input_patient_data.is_valid() is False:
                return render(request, 'main/update_patient.html', {'error_message': "Ошибка: Все поля должны быть заполнены."})
            pk=int(input_patient_data.cleaned_data['patient_id'])
            patient = Patient.objects.get(id=pk)
            if not patient:
                return render(request, 'main/update_patient.html', {'error_message': "Ошибка: такого пациента не существует."})
            data = {k: v for k, v in input_patient_data.cleaned_data.items() if k != "patient_id" and v}
            Patient.objects.filter(id=pk).update(**data)
            patient = Patient.objects.get(id=pk)
            return render(request, 'main/patient.html', {'patient': patient, 'is_new': False})
        return render(request, 'main/update_patient.html')

    @staticmethod
    @csrf_protect
    def create(request):
        if request.method == "POST":
            input_patient_data = PatientForm(request.POST)
            if input_patient_data.is_valid() is False:
                return render(request, 'main/new_patient.html',
                              {'error_message': "Ошибка: Все поля должны быть заполнены."})
            new_patient = Patient(
                **input_patient_data.cleaned_data
            )
            new_patient.save()
            return render(request, 'main/patient.html', {'patient': new_patient, 'is_new': True})
        return render(request, 'main/new_patient.html')
