from django.http import HttpResponse
from django.http import JsonResponse
from vacancies.models import Vacancy


# from django.shortcuts import render


def index(request):
    return HttpResponse('index page')


def hello(request):
    return HttpResponse('Hello, Dima')


def index_vacancies(request):
    """
    В request (класс) есть практически вся инфа о поступившем запросе
    objects - это формально ORM и в дальнейшем позволит нам обращаться к данным из БД
    """
    if request.method == 'GET':
        vacancies = Vacancy.objects.all()

        response = []
        for vacancy in vacancies:
            response.append(
                {
                    'id': vacancy.id,
                    'text': vacancy.text,
                }
            )
        # safe=False позволяет "скушать" JsonResponse словарь, говоря, что ничего не сломается при серриализации и
        # отключи все проверки при переводе в json
        return JsonResponse(response, safe=False)


def get_vacancies_from_id(request, vacancy_id):
    if request.method == 'GET':
        try:
            vacancy = Vacancy.objects.get(pk=vacancy_id)
        except Vacancy.DoesNotExist:
            return JsonResponse({
                'error': 'Not found'
            }, status=404)

        return JsonResponse({
            'id': vacancy.id,
            'text': vacancy.text,
        })
