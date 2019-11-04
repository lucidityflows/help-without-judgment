from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Requests
from .models import RequestForm
from django.http import HttpResponseRedirect

# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):

    user = request.user
    context = {'requests': Requests.objects.filter(requester=user)}

    return render(request, 'user/index.html', context)


def register(request):

    if request.method == "POST":

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')

    else:

        form = UserCreationForm()

    context = {'form': form}

    return render(request, 'registration/register.html', context)


def logout(request):

    logout(request)
    return redirect('/accounts/login')


def open_requests(request):

    user = request.user

    context = {'requests': Requests.objects.all().exclude(requester=user)}

    return render(request, 'user/open_requests.html', context)


def create_request(request):

    if request.method == "POST":

        form = RequestForm(request.POST)

        user = request.user

        if form.is_valid():

            type = form.cleaned_data['type']
            description = form.cleaned_data['description']
            current_request = form.save(commit=False)
            current_request.requester = user
            current_request.save()

            return HttpResponseRedirect('/')

    else:

        form = RequestForm()

    context = {'form': form}

    return render(request, 'user/create_request.html', context)
