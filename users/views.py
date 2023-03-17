from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

import csv
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

fs = FileSystemStorage(location="temp/")


def index(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user != None:
            auth_login(request, user)
            type = request.user.user_type
            if type == 'admin':
                return redirect('/admin_login/')
            elif type == 'user':
                return redirect('/userinfo/')
        if user == None:
            return HttpResponse("Not allowed")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/')
def adminDash(request):
    if request.user.user_type == 'admin':
        return render(request,
                      'admin_login.html',
                      context={
                        "user": CustomUser.objects.get(id = request.user.id)
                        })
    
    else:
        return HttpResponse("Not a valid User")


@login_required(login_url='/')
def addAdmin(request):
    if request.user.user_type == 'admin':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = CustomUser.objects.create_user(
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        username=username,
                                        password=password,
                                        user_type = "admin")
            user.save()
            
            return redirect('/addadmin/')
        else:
            admins = Admin.objects.all()
            context = {
                'users':admins,
            }
            return render(request, "addAdmin.html", context)
        
    else:
        return HttpResponse("Not a valid User")

@login_required(login_url='/')
def addUsers(request):
    if request.user.user_type == 'admin':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            contact = request.POST.get('number')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            user = CustomUser.objects.create_user(
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        username=username,
                                        password=password,
                                        user_type = "user")
            user.users.address=address
            user.users.gender=gender
            user.users.cantact_num=contact
            user.save()
            
            return redirect('/adduser/')
        else:
            users = Users.objects.all()
            context = {
                'users':users,
            }
            return render(request, "addUser.html", context)
    
    else:
        return HttpResponse("Not a valid User")


@login_required(login_url='/')
def addMultipleUser(request):
    if request.user.user_type == 'admin':
        if request.method == 'POST':
            file = request.FILES["files_csv"]
            content = file.read()
            
            file_content = ContentFile(content)
            file_name = fs.save(
                "_tmp.csv", file_content
            )
            tmp_file = fs.path(file_name)

            csv_file = open(tmp_file, errors="Ignore")
            reader = csv.reader(csv_file)
            next(reader)

            user_list = []

            for id_, row in enumerate(reader):
                (
                    firstname,
                    lastname,
                    email,
                    username,
                    password,
                    address,
                    gender,
                    contact
                ) = row

                user = CustomUser.objects.create_user(
                                        first_name=firstname,
                                        last_name=lastname,
                                        email=email,
                                        username=username,
                                        password=password,
                                        user_type = "user")
                user.users.address=address
                user.users.gender=gender
                user.users.cantact_num=contact
                user.save()

            return redirect('/adduser/')

        else:
            return HttpResponse("Page Note Reachable")
    else:
        return HttpResponse("Not a valid User")
    

@login_required(login_url='/')
def userInfo(request):
    id = request.user.id
    users = Users.objects.get(admin_id = id)

    context = {
        "user":users
    }
    return render(request, 'userInfo.html', context)