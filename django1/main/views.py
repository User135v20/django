import base64
import io
import json
from urllib.parse import unquote
from zipfile import ZipFile

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .forms import UserForm, UpdateUserForm, ResultForm, UpdateResultForm, ImageForm, DownloadImageForm, \
    DownloadImagesForm
from .models import Result, User, Image
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
        image_id = dict(request.GET).get('image_id')[0] if dict(request.GET).get('image_id') else None
        return render(request, 'main/create_result.html', {"image_id": image_id})

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
                    print(type(file))
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
    def render_images(request, results, error_message=None):
        data = {
            'all_results_list': results,
            'urls': json.dumps([str_to_base64(image.image.url) for image in results]),
            'image_count': len(results),
        }
        if error_message:
            data['error_message'] = error_message
        return render(request, 'main/all_images.html', data)

    @staticmethod
    def list(request):
        surname = dict(request.GET).get('surname')[0] if dict(request.GET).get('surname') else None
        image_ids = False
        results_query = Result.objects
        feature_names = ['structure_asymmetry', 'blue_white_structures', 'atypical_pigment_network', 'radial_radiance', 'points']
        for feature_name in feature_names:
            bool_feature = dict(request.GET).get(feature_name)[0] == "True" if dict(request.GET).get(feature_name) else None
            if bool_feature is not None:
                results_query = results_query.filter(**{feature_name: bool_feature})
                image_ids = True
        bool_description = dict(request.GET).get('description')[0] == "True" if dict(request.GET).get('description') else None
        if image_ids and bool_description is False:
            results = Image.objects.all()
            return render(request, 'main/all_images.html', {'all_results_list': results, 'image_count': len(results),
                                                            'error_message': "Был задан фильт на признаки в описания и одновременно включены описания"})
        if image_ids or bool_description is not None:
            image_ids = [r.image.id for r in results_query.all()]
        query = Image.objects
        if surname:
            query = query.filter(user__surname__contains=surname)
        if image_ids:
            if bool_description is False:
                query = query.exclude(id__in=image_ids)
            else:
                query = query.filter(id__in=image_ids)
        results = query.all()
        return render(request, 'main/all_images.html', {'all_results_list': results, 'image_count': len(results)})

    @staticmethod
    def delete(request, pk=None):
        result = Image.objects.get(id=pk)
        result.delete()
        results = Image.objects.all()
        return render(request, 'main/all_images.html', {'all_results_list': results, 'image_count': len(results)})

    @staticmethod
    @csrf_protect
    def download(request):
        if request.method == 'POST':
            form = DownloadImageForm(request.POST)
            if form.is_valid():
                # https://overcoder.net/q/1700285/%D0%BE%D1%82%D0%B2%D0%B5%D1%82%D0%BD%D1%8B%D0%B9-zip-%D1%84%D0%B0%D0%B9%D0%BB-%D0%BE%D1%82-django
                buffer = io.BytesIO()
                url = form.cleaned_data['image_id']
                with ZipFile(buffer, 'w') as zipObj:
                    zipObj.write("." + unquote(url)[6:])

                response = HttpResponse(content=buffer.getvalue())
                response['Content-Type'] = 'application/zip'
                response['Content-Disposition'] = 'attachment; filename=images.zip'
                return response
            else:
                query_parameter = dict(request.GET).get('surname')[0] if dict(request.GET).get('surname') else None
                results = Image.objects.filter(
                    user__surname__contains=query_parameter).all() if query_parameter else Image.objects.all()
                return ImageView.render_images(request, results, form.errors)
        else:
            query_parameter = dict(request.GET).get('surname')[0] if dict(request.GET).get('surname') else None
            results = Image.objects.filter(
                user__surname__contains=query_parameter).all() if query_parameter else Image.objects.all()
            return ImageView.render_images(request, results)

    @staticmethod
    @csrf_protect
    def download_images(request):
        form = DownloadImagesForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['urls'])
            urls = [base64_to_str(u) for u in json.loads(form.cleaned_data['urls'])]
            # https://overcoder.net/q/1700285/%D0%BE%D1%82%D0%B2%D0%B5%D1%82%D0%BD%D1%8B%D0%B9-zip-%D1%84%D0%B0%D0%B9%D0%BB-%D0%BE%D1%82-django
            buffer = io.BytesIO()
            with ZipFile(buffer, 'w') as zipObj:
                for url in urls:
                    zipObj.write("." + unquote(url)[6:])

            response = HttpResponse(content=buffer.getvalue())
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = 'attachment; filename=images.zip'
            return response

        else:
            query_parameter = dict(request.GET).get('surname')[0] if dict(request.GET).get('surname') else None
            results = Image.objects.filter(
                user__surname__contains=query_parameter).all() if query_parameter else Image.objects.all()
            return ImageView.render_images(request, results)


def normal_str_range():
    names = {k[: -4] for k in NORMAL_MEASURE}
    return {k: str(NORMAL_MEASURE[k + '_min']) + " - " + str(NORMAL_MEASURE[k + '_max']) for k in names}


def str_to_base64(message):
    # some images has russian names
    print(message)
    message_bytes = message.encode('utf-8')
    base64_bytes = base64.b64encode(message_bytes)
    s = base64_bytes.decode('utf-8')
    return s


def base64_to_str(message):
    return base64.b64decode(message).decode('utf-8')
