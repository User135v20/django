from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .forms import PatientForm, UpdatePatientForm, ResultForm, UpdateResultForm
from .models import Result, Patient
from .settings import NORMAL_MEASURE


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


class ResultView:
    @staticmethod
    def list(request):
        query_parameter = dict(request.GET).get('surname')[0] if dict(request.GET).get('surname') else None
        results = Result.objects.filter(
            patient__surname__contains=query_parameter) if query_parameter else Result.objects.all()
        return render(request, 'main/results.html', {'all_results_list': results})

    @staticmethod
    def get(request, pk):
        result = Result.objects.get(id=pk)
        for k, v in normal_str_range().items():
            setattr(result, k + "_norma", v)
        return render(request, 'main/result.html', {'result': result})

    @staticmethod
    @csrf_protect
    def create(request):
        if request.method == "POST":
            input_result_data = ResultForm(request.POST)
            if input_result_data.is_valid() is False:
                return render(request, 'main/create_result.html',
                              {'error_message': "Ошибка: Все поля должны быть заполнены."})

            data = input_result_data.cleaned_data
            patients = Patient.objects.filter(id=int(data['patient_id']))
            if not patients:
                return render(request, 'main/create_result.html',
                              {'error_message': "Ошибка: такого пациента не существует."})
            patient = patients[0]
            normal_range_ = normal_str_range()
            for k in normal_range_.keys():
                deviation = 0
                if data[k] > NORMAL_MEASURE[k + "_max"]:
                    deviation = data[k] - NORMAL_MEASURE[k + "_max"]
                if data[k] < NORMAL_MEASURE[k + "_min"]:
                    deviation = -data[k] + NORMAL_MEASURE[k + "_min"]
                data[k + '_deviation'] = deviation
            data['patient'] = patient
            del data['patient_id']
            result = Result(
                **data
            )
            result.save()
            for k, v in normal_range_.items():
                setattr(result, k + '_norma', v)
            return render(request, 'main/result.html', {'result': result})
        return render(request, 'main/create_result.html')

    @staticmethod
    def delete(request, pk=None):
        result = Result.objects.get(id=pk)
        result.delete()
        results = Result.objects.all()
        return render(request, 'main/results.html', {'all_results_list': results})

    @staticmethod
    @csrf_protect
    def update(request):
        if request.method == "POST":
            input_result_data = UpdateResultForm(request.POST)
            if input_result_data.is_valid() is False:
                return render(request, 'main/update_result.html',
                              {'error_message': "Ошибка: ошибка в врдимых данных."})
            patient_id = input_result_data.cleaned_data['patient_id']
            if patient_id:
                patients = Patient.objects.filter(id=patient_id)
                if not patients:
                    return render(request, 'main/update_result.html',
                                  {'error_message': "Ошибка: такого пациента не существует."})
            id_ = int(input_result_data.cleaned_data['id'])
            results = Result.objects.filter(id=id_)
            if not results:
                return render(request, 'main/update_result.html',
                              {'error_message': "Ошибка: такого результата не существует."})
            result = results[0]
            data = {k: v for k, v in input_result_data.cleaned_data.items() if k != "id" and v}
            if 'patient_id' in data and data['patient_id'] != result.patient.id:
                data['patient'] = patients[0]
                del data['patient_id']

            normal_range_ = normal_str_range()
            for k in normal_range_.keys():
                if k not in data.keys():
                    continue
                deviation = 0
                if data[k] > NORMAL_MEASURE[k + "_max"]:
                    deviation = data[k] - NORMAL_MEASURE[k + "_max"]
                if data[k] < NORMAL_MEASURE[k + "_min"]:
                    deviation = -data[k] + NORMAL_MEASURE[k + "_min"]
                data[k + '_deviation'] = deviation

            Result.objects.filter(id=id_).update(**data)
            result = Result.objects.get(id=id_)
            for k, v in normal_range_.items():
                setattr(result, k + '_norma', v)
            return render(request, 'main/result.html', {'result': result})
        return render(request, 'main/update_result.html')


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
                return render(request, 'main/update_patient.html',
                              {'error_message': "Ошибка: Все поля должны быть заполнены."})
            pk = int(input_patient_data.cleaned_data['patient_id'])
            patient = Patient.objects.get(id=pk)
            if not patient:
                return render(request, 'main/update_patient.html',
                              {'error_message': "Ошибка: такого пациента не существует."})
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


def normal_str_range():
    names = {k[: -4] for k in NORMAL_MEASURE}
    return {k: str(NORMAL_MEASURE[k + '_min']) + " - " + str(NORMAL_MEASURE[k + '_max']) for k in names}
