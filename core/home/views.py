from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

def resume(request):
    return render(request, "resume.html")

@login_required(login_url="/login/")
def student_data(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        age = data.get('age')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        en = Student(
            name = name,
            age = age,
            email = email,
            phone = phone,
            address = address,
        )
        en.save()

        return redirect('/student/')
    queryset = Student.objects.all()
    # if request.GET.get('search'):
    #     queryset = queryset.filter(name__icontains = request.GET.get('search'))
    context = {'Student': queryset}

    return render(request, "studentdata.html", context)

def delete_student(request, id):
    queryset = Student.objects.get(id = id)
    queryset.delete()
    return redirect('/student/')

def update_student(request, id):
    queryset = Student.objects.get(id = id)
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        age = data.get('age')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')

        queryset.name = name
        queryset.age = age
        queryset.email = email
        queryset.phone = phone
        queryset.address = address

        queryset.save()
        return redirect('/student/')
        
    context = {'Student': queryset}
    return render(request, "uppdatestudent.html", context)

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username", extra_tags="danger")
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, "Invalid Password", extra_tags="danger")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/student/')

    return render(request, "login.html")

def logoutpage(request):
    logout(request)
    return redirect('/login/')

def signuppage(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request, "Username Already Taken!", extra_tags="danger")
            return redirect('/signup/')

        user = User.objects.create(
            email = email,
            username = username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account Created Sucessfully!")
        return redirect('/signup/')

    return render(request, 'signup.html')