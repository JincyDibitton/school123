from django.contrib.auth import authenticate, login,logout, get_user_model
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserLoginForm, UserRegistrationForm
from .models import Department,Courses,Student
from.forms import StudentForm


# Create your views here.
def index(request):
    return render(request,"index.html")

User = get_user_model()
def register(request):
    form    = UserRegistrationForm(request.POST)

    context = {
            'form': form
        }

    if request.method == 'POST':
        #form = UserRegistrationForm(request.POST)

        if form.is_valid():
            username    = form.cleaned_data.get("username")
            email       = form.cleaned_data.get("email")
            password    = form.cleaned_data.get("password")
            print(username, password)
            new_user    = User.objects.create_user(username, email, password)
            return redirect("/login")
            
        else:
            print("Form is not valid")

    return render(request, 'register.html', context)

def login_view(request):
    form = UserLoginForm()

    context = {
            'form': form
        }

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            username    = form.cleaned_data.get("username")
            password    = form.cleaned_data.get("password")
            user        = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return redirect("/student_add")
            else:
                print("Error")

    return render(request, 'login.html', context)

    
def student_add(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request," Form saved !")
            return redirect('/confirm')
    return render(request, 'requirements.html', {'form': form})
def load_courses(request):
    department_id = request.GET.get('department_id')
    courses = Courses.objects.filter(department_id=department_id).all()
    return render(request,'courses_dropdown.html', {'courses':courses})
def logout(request):
    auth.logout(request)
    return redirect('/')
    
def confirm(request):
    return render(request,'confirm.html')