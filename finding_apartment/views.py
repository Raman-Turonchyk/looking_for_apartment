from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views import generic
from scraping.models import City, Link


def index(request):
    cities = City.objects.all()
    context = {'cities': cities}
    return render(request, 'finding_apartment/index.html', context=context)


def city(request, id: int):
    links = Link.objects.filter(city_id=id)
    paginator = Paginator(links, 20)
    page_number = request.GET.get('page')
    context = paginator.get_page(page_number)
    return render(request, 'finding_apartment/apartments_list.html', {'page_obj': context})
