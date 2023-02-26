import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from vacancies.models import Vacancy


def index(request):
    return HttpResponse('index page')


def hello(request):
    return HttpResponse('Hello, Dima')


@method_decorator(csrf_exempt, name='dispatch')  # переписали csrf_exempt под работу с классами
class VacancyView(View):  # наследуемся от базового класса View (generic views)
    def get(self, request):
        vacancies = Vacancy.objects.all()

        # реализуем поиск по вакансии по ее полному тексту (просто как пример)
        # get вызываем у атрибута .GET так как если этого не сделать, то падаем с ошибкой MultiValueDictKeyError
        # MultiValueDictKeyError - не передали text в квери-параметрах
        search_text = request.GET.get('text', None)
        if search_text is not None:
            vacancies = vacancies.filter(text=search_text)

        response = []
        for vacancy in vacancies:
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

    def post(self, request):
        # приводим данные из запроса к пито словарю и получаем в него данные
        vacancy_data = json.loads(request.body)

        # сохраняем в модель Вакансии(в поле text) полученные данные из словаря vacancy_data(ключ 'text')
        vacancy = Vacancy()
        vacancy.text = vacancy_data['text']
        # сохраняем нашу полученную вакансию в БД
        vacancy.save()
        return JsonResponse({
            'id': vacancy.id,
            'slug': vacancy.slug,
            'text': vacancy.text,
            'status': vacancy.status,
            'created': vacancy.created
        })


class VacancyDetailView(DetailView):  # наследуемся от DetailView - это класс для детального отображения элемента
    # в DetailView есть обязательный атрибут model, у него указывается название модели
    model = Vacancy

    def get(self, request, *args, **kwargs):  # вместо id теперь здесь *args, **kwargs
        # встроенный метод DetailView, который вернет нужный нам элемент (объект 1 вакансии)
        vacancy = self.get_object()

        return JsonResponse({
            'id': vacancy.id,
            'slug': vacancy.slug,
            'text': vacancy.text,
            'status': vacancy.status,
            'created': vacancy.created
        })
