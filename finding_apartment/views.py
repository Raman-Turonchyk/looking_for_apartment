from django.shortcuts import render


def index(request):
    return render(request, 'finding_apartment/index.html')
