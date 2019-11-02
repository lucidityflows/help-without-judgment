from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.




@login_required(login_url='/accounts/login/')
def index(request):

    return render(request, 'user/index.html')


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

    context = {'form' : form}

    return render(request, 'registration/register.html', context)


def logout(request):

    logout(request)
    return redirect('/accounts/login')
