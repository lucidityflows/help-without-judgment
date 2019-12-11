from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Requests
from .models import RequestForm, AcceptRequestForm, CancelRequestForm, CloseRequestForm, DeleteRequestForm, \
    ScheduleAppointmentForm, DateForm, ConfirmAppointmentForm
from django.http import HttpResponseRedirect
from itertools import chain
from datetime import datetime
from django.utils import timezone
from chat.models import Thread
from django import forms
from .forms import ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User
import requests
import json
from django.http import HttpResponse

# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):

    user = request.user

    if request.method == "POST":

        primary_key = request.POST["primary_key"]
        primary_key = int(primary_key)
        current_request = Requests.objects.get(pk=primary_key)

        if 'cancel' in request.POST:
            current_request.date_appointment = None
            current_request.appointment_confirmed = False
            current_request.accepter = None
            current_request.status = "Incomplete"
            current_request.appointment_suggested = False
            current_request.save()

        if 'delete' in request.POST:
            current_request.delete()

        if 'report' in request.POST:
            current_request.reported = True
            current_request.save()

        if 'message' in request.POST:

            if current_request.accepter == user.username:

                other_user = current_request.requester
                other_user = User.objects.get(username=other_user)

            else:

                other_user = current_request.accepter
                other_user = User.objects.get(username=other_user)

            potential_thread1 = Thread.objects.filter(first=user, second=other_user)
            potential_thread2 = Thread.objects.filter(first=other_user, second=user)

            if not potential_thread1 and not potential_thread2:

                new_thread = Thread(first=user, second=other_user)
                new_thread.save()

                return_url = '/messages/' + str(other_user)

                return HttpResponseRedirect(return_url)

            else:

                return_url = '/messages/' + str(other_user)

                return HttpResponseRedirect(return_url)

        if 'schedule' in request.POST:

            form = DateForm()

            if request.POST['new_date'] != '':
                new_date = request.POST['new_date']

                new_date = datetime.strptime(new_date, '%Y/%m/%d %H:%M').strftime('%Y-%m-%d %H:%M')
                # new_date = new_date[0:4] + "-" + new_date[5:7] + "-" + new_date[8:]
                current_request.date_appointment = new_date
                current_request.appointment_suggested = True
                current_request.status = "Appointment Not Yet Confirmed"
                current_request.save()

        if 'accept' in request.POST:

            current_request.appointment_confirmed = True
            current_request.status = "Confirmed"
            current_request.save()

        if 'reject' in request.POST:

            current_request.appointment_confirmed = False
            current_request.appointment_suggested = False
            current_request.date_appointment = None
            current_request.status = "Accepted"
            current_request.save()

        if 'cancel_appointment' in request.POST:

            current_request.appointment_confirmed = False
            current_request.date_appointment = None
            current_request.appointment_suggested = False
            current_request.status = "Accepted"
            current_request.save()

        if 'complete' in request.POST:

            current_request.status = "Complete"
            current_request.date_completed = datetime.now()
            current_request.save()

        return HttpResponseRedirect('/')

    else:

        accepted_query_list = Requests.objects.exclude(status="Complete").exclude(reported=True).filter(accepter=user)
        created_query_list = Requests.objects.exclude(status="Complete").exclude(reported=True).filter(requester=user)

        form = DateForm()
        #schedule_context = {'form': form}

        return render(request, 'user/index.html',
                      {'accepted_requests': accepted_query_list, 'created_requests': created_query_list, 'form': form})


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
        current_request.status = "Accepted"
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


def past_requests(request):

    if request.method == "POST":

        if request.POST['button'] == "accepter_feedback":

            feedback = request.POST['feedback_response']

            primary_key = request.POST["primary_key"]
            primary_key = int(primary_key)

            current_request = Requests.objects.get(pk=primary_key)
            current_request.accepter_feedback = feedback
            current_request.save()

        if request.POST['button'] == "requester_feedback":

            feedback = request.POST['feedback_response']

            primary_key = request.POST["primary_key"]
            primary_key = int(primary_key)

            current_request = Requests.objects.get(pk=primary_key)
            current_request.requester_feedback = feedback
            current_request.save()

        return render(request, 'user/index.html')

    else:

        user = request.user

        past_accepter_query_list = Requests.objects.filter(requester=user, status="Complete")
        past_requester_query_list = Requests.objects.filter(accepter=user, status="Complete")

        #context = past_accepter_query_list | past_requester_query_list
        #context = {'requests': context}

        return render(request, 'user/past_requests.html', {'accepted_requests': past_accepter_query_list, 'created_requests': past_requester_query_list})


@login_required(login_url='/accounts/login/')
def profile(request):

    if request.method == "POST":

        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return render(request, 'user/profile.html')

    else:

        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'user/profile.html', context)


def inbox(request):

    user = request.user

    message_thread_list_1 = Thread.objects.filter(first=user)
    message_thread_list_2 = Thread.objects.filter(second=user)

    message_list = message_thread_list_1 | message_thread_list_2

    return render(request, 'user/inbox.html', {'messages': message_list})


def non_profits(request):

    if request.method == "POST":

        charity_dict = {}
        city_input = request.POST["city_input"]
        state_input = request.POST["state_input"]

        json_response = get_nonprofits_from_zipcode(city_input, state_input)
        for item in json_response:
            name = item["charityName"]
            address = item["mailingAddress"]["streetAddress1"]
            city = item["mailingAddress"]["city"]
            zipcode = item["mailingAddress"]["postalCode"]
            website = item["websiteURL"]
            mission = item["mission"]
            new_dict = {"name": name, "address": address, "city": city, "zipcode": zipcode, "website": website, "mission": mission}
            #new_dict = {"name": [name, address, city, zipcode, website, mission]}
            charity_dict[name] = new_dict

        context = {'charities': charity_dict}
        #context = {'charities': json.dumps(charity_dict)
        return render(request, 'user/non_profits.html', {'charities': charity_dict})

    else:

        return render(request, 'user/non_profits.html')


def get_nonprofits_from_zipcode(city, state):

    charity_navigator_base_URL = "https://api.data.charitynavigator.org/v2"
    hwj_app_id = "app_id=d1284ae7"
    hwj_app_key = "app_key=ed550eb38ecf7e9e7c24ca4b40f2ce6e"
    api_method = "/Organizations"
    page_size = "pageSize=100"
    city = "city=" + city.lower()
    state = "state=" + state.upper()

    api_call = charity_navigator_base_URL + api_method + "?" + hwj_app_id + "&" + hwj_app_key + "&" + page_size + "&" + state + "&" + city
    response = requests.get(api_call)
    json_response = response.json()
    print(json_response)
    return json_response


