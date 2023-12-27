from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse("<h1><li><a href='/blogin/'>Blog</a></li> <li><a href='/login/'>Student Data</a></li></h1>")
def bloginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username", extra_tags="danger")
            return redirect('/blogin/')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, "Invalid Password", extra_tags="danger")
            return redirect('/blogin/')
        else:
            login(request,user)
            return redirect('/frontpage/')

    return render(request, "bloglogin.html")

def blogoutpage(request):
    logout(request)
    return redirect('/blogin/')

def blogsignuppage(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.error(request, "Username Already Taken!", extra_tags="danger")
            return redirect('/blogsignup/')

        user = User.objects.create(
            email = email,
            username = username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account Created Sucessfully!")
        return redirect('/blogsignup/')

    return render(request, 'blogsignup.html')

@login_required(login_url = '/blogin/' )
def frontpage(request):
    if request.method == "POST":
        data = request.POST
        title = data.get('title')
        slug = data.get('slug')
        intro = data.get('intro')
        body = data.get('body')
        image = request.FILES.get('image')

        data = Post(
            title = title,
            slug = slug,
            intro = intro,
            body = body,
            image = image,
        )

        data.save()
        return redirect('/frontpage/')
    queryset = Post.objects.all()
    context = {'Post': queryset}
    return render(request, 'frontpage.html',context)

def updatepost(request, id):
    queryset = Post.objects.get(id = id)
    if request.method == "POST":
        data = request.POST
        title = data.get('title')
        slug = data.get('slug')
        intro = data.get('intro')
        body = data.get('body')
        image = request.FILES.get('image')

        data = Post(
            title = title,
            slug = slug,
            intro = intro,
            body = body,
            image = image,
        )

        data.save()
        return redirect('/frontpage/')
    queryset = Post.objects.all()
    context = {'Post': queryset}
    return render(request, 'updatepost.html',context)


def deletepost(request, id):
    queryset = Post.objects.get(id = id)
    queryset.delete()
    return redirect('/frontpage/')

def postdetail(request, id):
    queryset = Post.objects.get(id=id)
    comments = Comments.objects.filter(post=queryset)  

    if request.method == "POST":
        form = request.POST
        name = form.get('name')
        body = form.get('body')

        new_comment = Comments(post=queryset, name=name, body=body)
        new_comment.save()


    context = {'Post': queryset, 'comments': comments}
    return render(request, 'postdetail.html', context)

def deletecomment(request, id):
    queryset = Comments.objects.get(id=id)
    queryset.delete()
    return redirect('postdetail', id=id)