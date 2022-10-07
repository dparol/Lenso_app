from msilib.schema import Condition
from turtle import update
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout  
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.http import JsonResponse
from django.contrib import messages
from .forms import create_user,update_data
from django.contrib.auth.forms import User
from .models import card


# Create your views here.
@never_cache
def user_login(request):
    
    if request.user.is_authenticated:
        return redirect(home)

    if request.method == 'POST':
        
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            
            return redirect('home')
        else:
            messages.error(request,'Enter a valid Username or Password')   
    return render(request, 'login.html')




    
@login_required(login_url='user_login')
def  user_logout(request):
    logout(request )
    return redirect('user_login')





def register(request):
    if request.user.is_authenticated:
        return redirect(home)
    else: 
        form = create_user()
        if request.method == 'POST':
            form = create_user(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,"Account is succesfully created for " +user)
                return redirect('user_login')
        context = {
            'form': form
        }
        return render(request, 'register.html',context)


@login_required(login_url='user_login')
@never_cache
def home(request):
    card_details=card.objects.all()
    return render(request,'home.html',{'card_dict':card_details})



@login_required(login_url='admin_login_user')
@never_cache
def admin_home(request):
    if request.user.is_superuser:
        search_key=request.GET.get('key') if request.GET.get('key')!=None else ''
        context = {
            'users':User.objects.filter(username__istartswith = search_key),
        }
        return render(request, 'admin_home.html',context)
    else:
        return redirect(admin_login_user)

@never_cache
def admin_login_user(request):
    if request.user.is_authenticated:
        return redirect(home)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')


            user = authenticate(request, username=username, password=password )
            if user is not None:
                if user.is_superuser:
                    login(request,user)
                    return redirect(admin_home)
                else:
                    messages.info(request,'Not an admin')
            else:
                messages.info(request, 'Wrong login credentisls')
        return render(request, 'admin_login.html')

@login_required(login_url='admin_login_user')
def user_delete(request,id):
    if request.user.is_superuser:
            if request.method=='POST':
                user_id = User.objects.get(pk=id)
                if user_id.is_superuser == True:
                    messages.info(request,"you can't delete user admin")
                    return redirect('admin_home')
                else:
                    
                    user_id.delete()
                    return redirect('admin_home')
    else:
        return redirect('admin_login_user')

@login_required(login_url='admin_login_user')
def user_update(request,id):
    if request.user.is_superuser:
        user_id = User.objects.get(pk=id)
        update_form = create_user(instance=user_id)
        if request.method == 'POST':
            update_form = update_data(request.POST,instance=user_id)
            if update_form.is_valid():
                update_form.save()
                return redirect('admin_home')
        context={
            'form':update_form
        }
        return render(request, 'user_update.html',context)
    else:
        return redirect('admin_login_user')

@login_required(login_url='admin_login_user')
def user_register(request):
    if request.user.is_superuser:
        form=create_user
        if request.method == 'POST':
            form=create_user(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin_home')
        context={'form':form}        
        return render(request,  'user_register.html',context)

