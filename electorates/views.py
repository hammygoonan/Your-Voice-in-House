from django.shortcuts import render
from electorates.models import Electorate, Member
from django.http import HttpResponse

def index(request):
    members = Electorate.objects.all()
    context = {'members': members}
    return render(request, 'electorates/index.html', context)