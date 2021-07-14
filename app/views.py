from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.



def login_student(request):
    if request.user.is_authenticated:
        return redirect('/all_student')
    else:
        if request.method =="POST":
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,'Student login Successfully')
                return redirect('/all_student')
            else:
                messages.error(request,'Invalid Credentials')
                return redirect('/login')
        return render(request,'login.html')



def register_student(request):
    if request.user.is_authenticated:
        return redirect('/all_student')
    else:
        if request.method=="POST":
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            address = request.POST['address']
            try:
                user_obj = User.objects.get(email = email)
                if user_obj:
                    messages.info(request,"This email is already exist try another")
                    return redirect('/signup')
            except:
                if password1 == password2:
                    user_data = User(username=email,first_name=username,password=make_password(password1))
                    user_data.save()
                    student_data = student(user=user_data,address=address)
                    student_data.save()
                    messages.success(request,'Student register successfully')
                    return redirect('/signup')
                else:
                    messages.error(request,'password and confirm password are not same')
                    return redirect('/signup')

        return render(request,'register.html')


def all_student(request):
    student_featch = student.objects.all()
    return render(request,'all_detail.html',{'stud':student_featch})

def student_remove(request,id):
    student_featch = User.objects.get(id=id)
    student_featch.delete()
    return redirect('/all_student')

def student_logout(request):
    logout(request)
    return redirect('/login')

def student_edit(request,id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        if request.method=="POST":
            id = request.POST.get('id')
            username = request.POST.get('username')
            address = request.POST.get('address')
            email = request.POST.get('email')
            print('ye email hai....',email)
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 != '' or password2 !='':
                if password1 == password2:
                    user_featch = User.objects.get(id=id)
                    student_featch = student.objects.get(user = user_featch)
                    if user_featch:
                        user_featch.first_name = username
                        user_featch.password = make_password(password1)
                        user_featch.save()
                        student_featch.address = address
                        student_featch.save()
                        login(request,user_featch)
                        messages.success(request,'Detail Update Successfully')
                        return redirect('/student_edit'+str(id))
                else:
                    messages.error(request,'Password and Confirm Password are not same')
                    return redirect('/student_edit'+str(id))
            else:
                user_featch = User.objects.get(id=id)
                student_featch = student.objects.get(user=user_featch)
                if user_featch:
                    user_featch.first_name = username
                    user_featch.save()
                    student_featch.address = address
                    student_featch.save()
                    messages.success(request, 'Detail Update Successfully')
                    return redirect('/student_edit' + str(id))
        return render(request, 'deatil_edit.html', {'data': user})
    else:
        return redirect('/login')