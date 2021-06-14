from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .forms import UserForm, UpdateUserForm, ResultForm, UpdateResultForm, ImageForm
from .models import Result, User,Image
from .settings import NORMAL_MEASURE


def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')


class ResultView:
    @staticmethod
    def list(request):
        query_parameter = dict(request.GET).get('surname')[0] if dict(request.GET).get('surname') else None
        image_id = dict(request.GET).get('image_id')[0] if dict(request.GET).get('image_id') else None
        query = Result.objects
        if query_parameter:
            query = query.filter(user__surname__contains=query_parameter)
        if image_id:
            query = query.filter(image__id__contains=int(image_id))
        results = query.all()
        print(len(results))
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
            users = User.objects.filter(id=int(data['user_id']))
            if not users:
                return render(request, 'main/create_result.html',
                              {'error_message': "Ошибка: такого пользователя не существует."})


            images = Image.objects.filter(id=int(data['image_id']))
            if not images:
                return render(request, 'main/create_result.html',
                              {'error_message': "Ошибка: такого изображения не существует."})

            user = users[0]
            normal_range_ = normal_str_range()
            for k in normal_range_.keys():
                deviation = 0
                if data[k] > NORMAL_MEASURE[k + "_max"]:
                    deviation = data[k] - NORMAL_MEASURE[k + "_max"]
                if data[k] < NORMAL_MEASURE[k + "_min"]:
                    deviation = -data[k] + NORMAL_MEASURE[k + "_min"]
                data[k + '_deviation'] = deviation
            data['user'] = user
            del data['user_id']
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
    def update(request, data=None):
        if request.method == "POST":
            input_result_data = UpdateResultForm(request.POST)
            if input_result_data.is_valid() is False:
                return render(request, 'main/update_result.html',
                              {'error_message': f"Ошибка: ошибка в водимых данных. {input_result_data.errors}"})
            user_id = input_result_data.cleaned_data['user_id']
            if user_id:
                users = User.objects.filter(id=user_id)
                if not users:
                    return render(request, 'main/update_result.html',
                                  {'error_message': "Ошибка: такого пользователя не существует."})
            id_ = int(input_result_data.cleaned_data['result_id'])
            results = Result.objects.filter(id=id_)
            if not results:
                return render(request, 'main/update_result.html',
                              {'error_message': "Ошибка: такого результата не существует."})
            result = results[0]
            data = {k: v for k, v in input_result_data.cleaned_data.items() if k != "result_id" and v}
            if 'user_id' in data and data['user_id'] != result.user.id:
                data['user'] = users[0]
                del data['user_id']

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
        if data:
            return render(request, 'main/update_result.html', data)
        return render(request, 'main/update_result.html')


class UserView:
    @staticmethod
    def list(request):
        query_parameter = dict(request.GET).get('surname')[0] if dict(request.GET).get('surname') else None
        if query_parameter:
            results = User.objects.filter(surname__contains=query_parameter).all()
        else:
            results = User.objects.all()
        return render(request, 'main/users.html', {'users': results})

    @staticmethod
    def delete(request, pk=None):
        user = User.objects.get(id=pk)
        user.delete()
        users = User.objects.all()
        return render(request, 'main/users.html', {'users': users})

    @staticmethod
    @csrf_protect
    def update(request):
        if request.method == "POST":
            input_user_data = UpdateUserForm(request.POST)
            if input_user_data.is_valid() is False:
                return render(request, 'main/update_user.html',
                              {'error_message': "Ошибка: Все поля должны быть заполнены."})
            pk = int(input_user_data.cleaned_data['user_id'])
            user = User.objects.filter(id=pk).first()
            if not user:
                return render(request, 'main/update_user.html',
                              {'error_message': "Ошибка: такого пользователя не существует."})
            data = {k: v for k, v in input_user_data.cleaned_data.items() if k != "user_id" and v}
            User.objects.filter(id=pk).update(**data)
            user = User.objects.get(id=pk)
            return render(request, 'main/user.html', {'user': user, 'is_new': False})
        return render(request, 'main/update_user.html')

    @staticmethod
    @csrf_protect
    def create(request):
        if request.method == "POST":
            input_user_data = UserForm(request.POST)
            if input_user_data.is_valid() is False:
                return render(request, 'main/new_user.html',
                              {'error_message': "Ошибка: Все поля должны быть заполнены."})
            new_user = User(
                **input_user_data.cleaned_data
            )
            new_user.save()
            return render(request, 'main/user.html', {'user': new_user, 'is_new': True})
        return render(request, 'main/new_user.html')


class ImageView:
    @staticmethod
    @csrf_protect
    def add(request):
        """Process images uploaded by users"""
        if request.method == 'POST':
            # form = ImageForm(request.POST)
            # TODO: на настоящий момент не нашел сериалайзер для листа картинок. как будет время - надо вставить
            if request.POST.get('user_id') and request.FILES:
                user_id = request.POST.get('user_id')
                user = User.objects.filter(id=user_id)
                if not user:
                    return render(request, 'main/add_image.html',
                                  {'error_message': "Ошибка: такого пользователя не существует."})
                user = user[0]
                images = []
                for file in request.FILES.getlist('images'):
                    data = {'image': file, 'user': user}
                    image = Image(**data)
                    image.save()
                    images.append(image)
                return render(request, 'main/add_image.html', {'images': images})
            # else:
            #     return render(request, 'main/add_image.html', {'form': form, 'error_message': form.errors})
        else:
            form = ImageForm()
        return render(request, 'main/add_image.html')

    @staticmethod
    def list(request):
        query_parameter = dict(request.GET).get('surname')[0] if dict(request.GET).get('surname') else None
        results = Image.objects.filter(user__surname__contains=query_parameter).all() if query_parameter else Image.objects.all()
        return render(request, 'main/all_images.html', {'all_results_list': results})

    @staticmethod
    def delete(request, pk=None):
        result = Image.objects.get(id=pk)
        result.delete()
        results = Image.objects.all()
        return render(request, 'main/all_images.html', {'all_results_list': results})



def normal_str_range():
    names = {k[: -4] for k in NORMAL_MEASURE}
    return {k: str(NORMAL_MEASURE[k + '_min']) + " - " + str(NORMAL_MEASURE[k + '_max']) for k in names}
