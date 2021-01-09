from django.http import Http404
from django.shortcuts import render
from .forms import PatientForm
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
    if not results:
        raise Http404("Results does not exist")
    return render(request, 'main/results.html', {'all_results_list': results})


def patients(request):
    results = Patient.objects.all()
    return render(request, 'main/patients.html', {'patients': results})


def delete_patient(request, pk = None):
    patient = Patient.objects.get(id=pk)
    if not patient:
        return Http404()
    patient.delete()
    patients = Patient.objects.all()
    return render(request, 'main/patients.html', {'patients': patients})


@csrf_protect
def new_patient(request):
    if request.method == "POST":
        input_patient_data = PatientForm(request.POST)
        if input_patient_data.is_valid() is False:
            raise Exception("asas")
        new_patient = Patient(
            **input_patient_data.cleaned_data
        )
        new_patient.save()
        return render(request, 'main/patient.html', {'patient': new_patient, 'is_new': True})
    else:
        new_patient = PatientForm()
    return render(request, 'main/new_patient.html')

