from django.shortcuts import render, get_object_or_404
from scraping.models import City, Link


def index(request):
    cities = City.objects.all()
    context = {'cities': cities}
    return render(request, 'finding_apartment/index.html', context=context)


def city(request, id: int):
    links = Link.objects.filter(city_id=id)
    context = {'links': links}
    return render(request, 'finding_apartment/looking_page.html', context=context)

def f(request):
    return render(request, 'finding_apartment/feedback.html')
