from datetime import date

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as login_auth, authenticate, logout, login
from django.conf import settings
from .forms import AccountAuthenticationForm, RegistrationForm, CreateQueForm, AccountUpdateForm
from django.db import models
from dateutil.relativedelta import *
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from matchsystem.utils import get_match_request_or_false
from matchsystem.match_request_status import MatchRequestStatus
import os
import cv2
import json
import base64
from django.core import files

from django.forms import ModelForm
from .models import users, Questiones,  questionnaire
from matchsystem.models import MatchList,MatchRequest

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png "
def home(request):
    return render(request, 'profiles/homepage.html')


def aboutus(request):
    return render(request, 'profiles/aboutus.html')


def reports(request):
    context={}
    alluser=users.objects.filter(is_active=True)
    context={
        alluser:alluser
    }
    print(context)
    return render(request, 'profiles/reports.html',context)


def contactus(request):
    return render(request, 'profiles/contactus.html')


def price(request):
    return render(request, 'profiles/price.html')


def Questionnaire(request):
    context = {}
    que1 = Questiones.objects.filter(id=1).first()
    que2 = Questiones.objects.filter(id=2).first()
    que3 = Questiones.objects.filter(id=3).first()
    que4 = Questiones.objects.filter(id=4).first()
    que5 = Questiones.objects.filter(id=5).first()
    que6 = Questiones.objects.filter(id=6).first()
    que7 = Questiones.objects.filter(id=7).first()
    userid=request.user.userId
    context['question1'] = que1.question
    context['q1o1'] = que1.option_one
    context['q1o2'] = que1.option_two
    context['q1o3'] = que1.option_three
    context['question2'] = que2.question
    context['q2o1'] = que2.option_one
    context['q2o2'] = que2.option_two
    context['q2o3'] = que2.option_three
    context['question3'] = que3.question
    context['q3o1'] = que3.option_one
    context['q3o2'] = que3.option_two
    context['q3o3'] = que3.option_three
    context['question4'] = que4.question
    context['q4o1'] = que4.option_one
    context['q4o2'] = que4.option_two
    context['q4o3'] = que4.option_three
    context['question5'] = que5.question
    context['q5o1'] = que5.option_one
    context['q5o2'] = que5.option_two
    context['q5o3'] = que5.option_three
    context['question6'] = que6.question
    context['q6o1'] = que6.option_one
    context['q6o2'] = que6.option_two
    context['q6o3'] = que6.option_three
    context['question7'] = que7.question
    context['q7o1'] = que7.option_one
    context['q7o2'] = que7.option_two
    context['q7o3'] = que7.option_three
    if request.method == 'POST':
        ans1 = request.POST.get('question1')
        ans2 = request.POST.get('question2')
        ans3 = request.POST.get('question3')
        ans4 = request.POST.get('question4')
        ans5 = request.POST.get('question5')
        ans6 = request.POST.get('question6')
        ans7 = request.POST.get('question7')
        id=request.user.userId
        print(id)
        if not questionnaire.objects.filter(user=id).exists():
            queans = questionnaire.objects.create(question1=ans1, question2=ans2, question3=ans3, question4=ans4,question5=ans5, question6=ans6, question7=ans7, user_id=id)
            queans.save()
            return redirect("Profile", userId=id)
        else:
            return HttpResponse("You already have filled the form")

    return render(request, 'profiles/questionnaire.html', context)

def updateque(request):
    Ques = Questiones.objects.filter(is_deleted=0)
    return render(request, 'profiles/update_que.html', locals())

def CreateQue(request):
    Ques = Questiones.objects.all()
    if request.method == 'POST':
        form = CreateQueForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CreateQueForm()
    # context = {
    #     'form': form
    # }
    return render(request, 'profiles/createque.html',locals())


def ProfilePage(request, *args, **kwargs):
    context = {}
    id = kwargs.get("userId")
    try:
        account = users.objects.get(userId=id)
    except Exception as e:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.userId
        context['FirstName'] = account.FirstName
        context['username'] = account.username
        context['LastName'] = account.LastName
        context['DOB'] = account.DOB
        context['email'] = account.email
        context['Address'] = account.Address
        context['Country'] = account.Country
        context['City'] = account.City
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email
        context['about_me'] = account.about_me
        context['PostalCode'] = account.PostalCode
        try:
            match_list = MatchList.objects.get(user=account)
            print(match_list)
        except MatchList.DoesNotExist:
            match_list = MatchList(user=account)
            match_list.save()
        matches=match_list.matches.all()
        context['matches'] = matches
        # Define template variables
        is_self = True
        is_match = False
        request_sent = False
        match_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            if matches.filter(pk=user.pk):
                is_match=True
            else:
                is_match=False
                if get_match_request_or_false(sender=account,receiver=user) != False:
                    request_sent = MatchRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_match_request_id']=get_match_request_or_false(sender=account,receiver=user).id
                elif get_match_request_or_false(sender=user, receiver=account) != False:
                    request_sent = MatchRequestStatus.YOU_SENT_TO_THEM.value
                else:
                    request_sent = MatchRequestStatus.NO_REQUEST_SENT.value
        elif not user.is_authenticated:
            is_self = False
        else:
            try:
                match_requests = MatchRequest.objects.filter(receiver=user, is_active=True)
            except:
                pass

        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_match'] = is_match

        context['request_sent'] = request_sent
        context['match_requests'] = match_requests
        context['BASE_URL'] = settings.BASE_URL
        print(context)




    user1=questionnaire.objects.filter(user=id).first()
    user2=questionnaire.objects.filter(user=request.user.userId).first()

    matchp=0
    if user1.question1 == user2.question1:
        matchp+=1
    if user1.question2 == user2.question2:
        matchp+=1
    if user1.question3 == user2.question3:
        matchp+=1
    if user1.question4 == user2.question4:
        matchp+=1
    if user1.question5 == user2.question5:
        matchp+=1
    if user1.question6 == user2.question6:
        matchp+=1
    if user1.question7 == user2.question7:
        matchp+=1
    MatchPer =int((" %.0f" % (100 * float(matchp) / 7)))
    context['MatchPer'] = MatchPer
    # match = matches.objects.filter(Q(user1_id=request.user.userId)| Q(user1_id=id)).filter(Q(user2_id=request.user.userId)| Q(user2_id=id))
    # if match:
    #     is_matched=True
    #     context['is_matched'] =is_matched
    #     print(context)
    return render(request, 'profiles/profile_page.html',context)

def Edit(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    id = kwargs.get("userId")
    account = users.objects.filter(userId=id).first()
    if account.userId != request.user.userId:
        return HttpResponse("You cant change this User Profile")
    if request.POST:
        form = AccountUpdateForm(request.POST or None, request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("Profile",userId=id)
        else:
            form= AccountUpdateForm(request.POST or None , instance=request.user,
                                    initial = {
                                        "id": account.userId,
                                        "FirstName": account.FirstName,
                                        "username": account.username,
                                        "LastName": account.LastName,
                                        "DOB": account.DOB,
                                        "email": account.email,
                                        "Address": account.Address,
                                        "Country": account.Country,
                                        "City": account.City,
                                        "profile_image": account.profile_image,
                                        "about_me": account.about_me,
                                        "PostalCode": account.PostalCode,
                                    }
                                    )
            context['form'] = form
            print(form)
    else:
        form= AccountUpdateForm(
                        initial={
                            "id" : account.userId,
                            "FirstName" : account.FirstName,
                            "username" : account.username,
                            "LastName" : account.LastName,
                            "DOB" : account.DOB,
                            "email" : account.email,
                            "Address" : account.Address,
                            "Country" : account.Country,
                            "City" : account.City,
                            "profile_image" : account.profile_image,
                            "about_me" : account.about_me,
                            "PostalCode" : account.PostalCode,
                        }
                        )
        context['form'] = form
    context['DATA_UPLOAD_MAX_MEMORY_SIZE']=settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    return render(request, 'profiles/edit_profile_page.html',context)

def Chat(request):
    return render(request, 'profiles/chat_page.html')


def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            profiles = authenticate(email=email, password=raw_password)
            login_auth(request, profiles)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('Questionnaire')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'profiles/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect("home")


def login_view(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")

    # print("destination: " + str(destination))
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                destination = get_redirect_if_exists(request)
                if destination:
                    return redirect(destination)
                return redirect("home")
        else:
            context['login_form'] = form
    return render(request, "profiles/login.html", context)


def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
        if request.GET.get("next"):
            redirect = str(request.GET.get("next"))
    return redirect


def save_temp_profile_image_from_base64String(imageString, user):
    INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
    try:
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
            os.mkdir(settings.TEMP + "/" + str(user.pk))
        url = os.path.join(settings.TEMP + "/" + str(user.pk), TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url
    except Exception as e:
        print("exception: " + str(e))
        # workaround for an issue I found
        if str(e) == INCORRECT_PADDING_EXCEPTION:
            imageString += "=" * ((4 - len(imageString) % 4) % 4)
            return save_temp_profile_image_from_base64String(imageString, user)
    return None


def crop_image(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get("image")
            url = save_temp_profile_image_from_base64String(imageString, user)
            img = cv2.imread(url)

            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))
            if cropX < 0:
                cropX = 0
            if cropY < 0:  # There is a bug with cropperjs. y can be negative.
                cropY = 0
            crop_img = img[cropY:cropY + cropHeight, cropX:cropX + cropWidth]

            cv2.imwrite(url, crop_img)

            # delete the old image
            user.profile_image.delete()

            # Save the cropped image to user model
            user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
            user.save()

            payload['result'] = "success"
            payload['cropped_profile_image'] = user.profile_image.url

            # delete temp file
            # os.remove(url)

        except Exception as e:
            print("exception: " + str(e))
            payload['result'] = "error"
            payload['exception'] = str(e)
    return HttpResponse(json.dumps(payload), content_type="application/json")

