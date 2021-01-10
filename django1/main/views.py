from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Patient
# Create your views here.

class PatientView(ListView):
    model = Patient
    template_name = 'Patient_database.html'
    context_object_name = 'patients'
    def list(request):
        return render(request, 'main/Patient_database.html', {'Patients': Patient.objects.all()})



def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/Patient_database.html')