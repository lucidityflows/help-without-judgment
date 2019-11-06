from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Requests
from .models import RequestForm, AcceptRequestForm, CancelRequestForm, CloseRequestForm, DeleteRequestForm
from django.http import HttpResponseRedirect
from itertools import chain

# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):

    if request.method == "POST":

        if request.POST['button'] == "cancel":

            form = CancelRequestForm(request.POST)

            user = request.user
            primary_key = form.data["primary_key"]
            primary_key = int(primary_key)
            form.accepter = user

            current_request = Requests.objects.get(pk=primary_key)
            current_request.accepter = None
            current_request.status = "Incomplete"
            current_request.save()

        if request.POST['button'] == "delete":

            form = DeleteRequestForm(request.POST)

            user = request.user
            primary_key = form.data["primary_key"]
            primary_key = int(primary_key)
            form.requester = user

            current_request = Requests.objects.filter(pk=primary_key)
            current_request.delete()

        return HttpResponseRedirect('/')



    else:

        user = request.user
        created_query_list = Requests.objects.filter(requester=user)
        accepted_query_list = Requests.objects.filter(accepter=user)

        context = created_query_list | accepted_query_list
        context = {'requests': context}

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

    if request.method == "GET":

        user = request.user

        context = Requests.objects.all().exclude(requester=user).filter(accepter=None)
        context = {'requests': context}

        #context = {'requests': Requests.objects.all().exclude(requester=user)}

        return render(request, 'user/open_requests.html', context)

    if request.method == "POST":

        form = AcceptRequestForm(request.POST)

        user = request.user
        primary_key = form.data["primary_key"]
        primary_key = int(primary_key)
        form.accepter = user

        current_request = Requests.objects.get(pk=primary_key)
        current_request.accepter = str(user)
        current_request.save()

        return HttpResponseRedirect('/')


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

