import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from vacancies.models import Vacancy, Skill


def index(request):
    return HttpResponse('index page')


def hello(request):
    return HttpResponse('Hello, Dima')


@method_decorator(csrf_exempt, name='dispatch')  # переписали csrf_exempt под работу с классами
class VacancyListView(ListView):  # наследуемся от базового класса View (generic views)
    model = Vacancy

    def get(self, request, *args, **kwargs):
        # vacancies = Vacancy.objects.all() - вместо этой строчки мы пишем вызов родителя VacancyView
        super().get(request, *args, **kwargs)

        search_text = request.GET.get('text', None)
        if search_text is not None:
            self.object_list = self.object_list.filter(text=search_text)

        response = []
        for vacancy in self.object_list:
            response.append(
                {
                    'id': vacancy.id,
                    'slug': vacancy.slug,
                    'text': vacancy.text,
                    'status': vacancy.status,
                    'created': vacancy.created
                }
            )
        # safe=False позволяет "скушать" JsonResponse словарь, говоря, что ничего не сломается при серриализации и
        # отключи все проверки при переводе в json
        return JsonResponse(response, safe=False)


class VacancyDetailView(DetailView):  # наследуемся от DetailView - это класс для детального отображения элемента
    # в DetailView есть обязательный атрибут model, у него указывается название модели
    model = Vacancy

    def get(self, request, *args, **kwargs):  # вместо id теперь здесь *args, **kwargs
        # встроенный метод DetailView, который вернет нужный нам элемент (объект 1 вакансии)
        try:
            vacancy = self.get_object()
        except Vacancy.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

        return JsonResponse({
            'id': vacancy.id,
            'slug': vacancy.slug,
            'text': vacancy.text,
            'status': vacancy.status,
            'created': vacancy.created
        })


# отдельный класс для POST
@method_decorator(csrf_exempt, name='dispatch')
class VacancyCreateView(CreateView):
    model = Vacancy  # модель с которой будет работать CreateView
    fields = ['user', 'slug', 'text', 'status', 'created', 'skills']  # чтобы CreateView автоматически генерил форму
    # в уроках формы мы исп. не будем, но данный атрибут обязательный, так что не юзать мы его не можем

    def post(self, request, *args, **kwargs):  # *args, **kwargs - обязательные аргументы, которые передаются во вьюху
        # приводим данные из запроса к пито словарю и получаем в него данные
        vacancy_data = json.loads(request.body)

        # сохраняем в модель все данные полученные постом от пользователя (create - вызывает save автоматически)
        vacancy = Vacancy.objects.create(
            user_id=vacancy_data['user_id'],
            slug=vacancy_data['slug'],
            text=vacancy_data['text'],
            status=vacancy_data['status'],
        )
        return JsonResponse({
            'id': vacancy.id,
            'slug': vacancy.slug,
            'text': vacancy.text,
            'status': vacancy.status,
            'created': vacancy.created
        })


@method_decorator(csrf_exempt, name='dispatch')
class VacancyUpdateView(UpdateView):
    model = Vacancy  # модель с которой будет работать CreateView
    fields = ['slug', 'text', 'status', 'skills']  # чтобы CreateView автоматически генерил форму

    def patch(self, request, *args, **kwargs):  # *args, **kwargs - обязательные аргументы, которые передаются во вьюху
        super().post(request, *args, **kwargs)  # с помощью этого достаем нужный элемент для обновления

        vacancy_data = json.loads(request.body)

        self.object.slug = vacancy_data['slug']
        self.object.text = vacancy_data['text']
        self.object.status = vacancy_data['status']

        for skill in vacancy_data['skills']:
            try:
                skill_obj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                return JsonResponse({'error': 'Skill not found'}, status=404)
            self.object.skills.add(skill_obj)

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'text': self.object.text,
            'slug': self.object.slug,
            'status': self.object.status,
            'created': self.object.created,
            'user': self.object.user_id,
            'skills': list(self.object.skills.all().values_list('name', flat=True)),
        })


@method_decorator(csrf_exempt, name='dispatch')
class VacancyDeleteView(DeleteView):
    model = Vacancy
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)  # вызываем родительский метод

        return JsonResponse({'status': 'ok'}, status=200)
