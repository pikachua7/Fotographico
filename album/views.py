from django.shortcuts import render,redirect
from .models import Category,Photo
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('gallery')
    else:
        form=CreateUserForm()
        if request.method =='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request,'Account was created for '+ user)
                return redirect('login')

        context={'form':form}
    return render(request,'album/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('gallery',user_id=request.user.id)
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('gallery',user_id=request.user.id)
            else:
                messages.info(request,'Username or Password is incorrect')
        context={}
        return render(request,'album/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def gallery(request,user_id):
    category=request.GET.get('category')
    user_photos = Photo.objects.filter(user__username__contains=request.user.username)
    if category==None:
        photos=user_photos
    else:
        photos = user_photos.filter(category__name=category)
    
    categories=Category.objects.filter(user__username__contains=request.user.username)
    context={'categories':categories,'photos':photos,'user_id':user_id}
    return render(request,'album/gallery.html',context)

@login_required(login_url='login')
def viewPhoto(request,pk):
    photo = Photo.objects.get(id=pk)
    return render(request,'album/photo.html',{'photo':photo,'user_id':request.user.id})

@login_required(login_url='login')
def addPhoto(request):
    categories=Category.objects.filter(user__username__contains=request.user.username)

    if request.method =='POST':
        data=request.POST
        images=request.FILES.getlist('images')
        if data['category']!= 'none':
            category=Category.objects.get(id=data['category'])
        elif data['category_new']!='':
            category,created=Category.objects.get_or_create(name=data['category_new'],user=User.objects.get(id=request.user.id))
        else:
            category=None

        for image in images:
            photo = Photo.objects.create(
                user=User.objects.get(id=request.user.id),
                category=category,
                description=data['description'],
                image=image,
            )
        return redirect('gallery',user_id=request.user.id)

    context={'categories':categories,'user_id':request.user.id}
    return render(request,'album/add.html',context)

def homePage(request):
    return render(request,'album/home.html',{})