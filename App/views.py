from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login,get_user_model
from django.contrib.auth.decorators import permission_required,login_required
from django.contrib.auth.forms import UserCreationForm
from App.models import GMail #Signup,
from django.contrib import messages

import csv, io
from django.utils.translation import pgettext_lazy
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from validate_email_address import validate_email
import  re, smtplib, logging, socket

# Create your views here.

valid_list = []
invalid_list = []
logged_out = True

def home(request):
    global logged_out
    global valid_list
    valid_list = []
    global invalid_list 
    invalid_list = []
    logged_out = True
    return render(request,'home.html')


# regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        
pattern = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"

def file(request):
    if request.method == "POST":
        
        file = request.FILES["myfile"]
        if not file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
            return redirect('/file')
        
        messages.success(request, 'CSV file uploaded and updated')
        todelete = GMail.objects.all()
        todelete.delete()
        fss = FileSystemStorage()
        # file = fss.save(file.name, file)
        data_set = file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        global valid_list
        valid_list = []
        global invalid_list 
        invalid_list = []
        for row in csv.reader(io_string):
            mail = row
            check = ''.join(mail) 
            if re.match(pattern, check):
                valid_list += mail
                GMail(email = check).save()
            else:
                invalid_list += mail
    return render(request,'file.html') 


def index(request):
    if logged_out:
        return HttpResponse("<h1>Please Login First!</h1>")
    else:
        return render(request, 'index.html')

def loginUser(request):
    if request.method == "POST":
        usrname = request.POST.get('username')
        pswd = request.POST.get('password')
        user = False
        if User.objects.get(username=usrname, password=pswd):
            user = True
        if user:
            global logged_out
            logged_out = False
            return render(request, 'index.html')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def logoutUser(request):
    return redirect('/login')

def about(request):
    return render(request, 'about.html')

def check_username(request):
    usrnm = request.POST.get('su_username')
    if get_user_model.objects.filter(username = usrnm).exists():
        return HttpResponse('<div style="color:red">This Username already exists</div>') 
    else:
        return HttpResponse('<div style="color:green">Valid Username</div>')

def signup(request):
    if request.method == "POST":
        su_username = request.POST.get('su_username')
        su_password = request.POST.get('su_password')
        signup = User(username = su_username, password = su_password)
        signup.save()
        messages.success(request, 'Sign In successfull!')
    return render(request, 'signup.html')


def validate(request):
    email_list = GMail.objects.all()
    return render(request, 'validate.html', {'valid_list': valid_list})


def invalid(request):
    return render(request,'invalid.html',{'invalid_list' : invalid_list})


def emails(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        msg = request.POST.get('msg')
        attac = request.FILES["attach"]
        
        valid_email = GMail.objects.all().values_list()
        
        id = GMail.objects.values_list('email', flat=True)
        email = EmailMessage(subject,msg,'pramodrajkothari99@gmail.com',valid_list)
        email.content_subtype ="html"
        email.attach(attac.name,attac.read(),attac.content_type)
        email.send(fail_silently=False)
        messages.success(request, 'Message Sent successfully !')
        global logged_out
        logged_out = False
    return render(request, 'emails.html')


