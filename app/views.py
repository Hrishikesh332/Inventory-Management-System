from django.shortcuts import render,redirect,HttpResponse
from django.core.mail import send_mail
from .models import Enquiry
from django.contrib import messages
import uuid

from django.contrib.auth.forms import UserCreationForm

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import requests
import json
import os
from .models import Enquiry

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
@login_required(login_url='login')

def SignupPage(request):
    if request.method=='POST':
        uname= request.POST.get('username')
        email= request.POST.get('email')
        pass1= request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Password is not same")
        else:
            my_user=User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
        if request.method=='POST':
            username=request.POST.get('username')
            pass1=request.POST.get('pass')
            user=authenticate(request,username=username,password=pass1)
            if user is not None:
                login(request, user)
                return redirect('/emp1')
            else:
                return HttpResponse ("Username or Password is incorrect")
        return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


def sendmail(enquiry_no):
    #email section
    user = Enquiry.objects.all().values().last()
    # if(user['enquiry_no']==True):

    print(user,"<<< data")
    print("++++++++++++++++++++++++++++++++++++++++", user['email'])
    html_content =render_to_string("email.html",{'title':'Conformation mail', 'name':user['name'] , 'detail':user['enquiry_details'], 'email':user['email'], 'enquiry_no':user['enquiry_no'], 'quotation_no':user['quotation_no'] })
    text_content =strip_tags(html_content)
    email=EmailMultiAlternatives(
            #subject
            "Enquiry Recived",
            #content
            "Thank you, for filling the form",
            #from email
            "hriskikesh.yadav332@gmail.com",
            #rec_list
            [user['email']])
    email.attach_alternative(html_content,"text/html")
    email.send()
    # else:
    #     print("Email not send")





# class Enquiry(models.Model):
#     name = models.CharField(max_length=255)
#     product_details = models.TextField()
#     other_specifications = models.TextField()
#     enquiry_number = models.CharField(max_length=255)
#     quotation_number = models.CharField(max_length=255)

# def get_enquiry_data(form_url):
#     response = requests.get(form_url)
#     data = response.json()
#     return data

# def save_enquiry_data(data):
#     enquiry = Enquiry(
#         name=data['name'],
#         product_details=data['product_details'],
#         other_specifications=data['other_specifications'],
#     )
#     enquiry.save()

# def send_confirmation_email(enquiry):
#     subject = 'Enquiry Confirmation'
#     message = f'Your enquiry has been received. Your enquiry number is {enquiry.enquiry_number} and your quotation number is {enquiry.quotation_number}.'
#     send_mail(subject, message, 'no-reply@example.com', [enquiry.email])



def index(request):
    return render(request,'index.html')

def enquiry(request):
    if request.method=='POST':
        enquiry=Enquiry()
        enquiry.name=request.POST.get('name')
        enquiry.email=request.POST.get('email')
        enquiry.phone=request.POST.get('phone')
        enquiry.enquiry_details=request.POST.get('enquiry_details')

        # Generate enquiry number
        enquiry.enquiry_no = str(uuid.uuid4())
        # enquiry.enquiry_no = enquiry_no  

        quotation_no = str(uuid.uuid4())
        quotation_no = "QN-" + enquiry.name[:6]+ quotation_no[:4]
        enquiry.quotation_no = quotation_no
        # print(enquiry.quotation_no)
        enquiry.save()
        messages.success(request, "Enquiry Sent Succesfully." )
        sendmail(enquiry.enquiry_no)
        return redirect ('/')
    else:
        return render(request,'enquiry.html')



# def sendmail(id):

#     user=Enquirys.objects.all().values()

#     if (user['name']==True):
#         html_content = render_to_string("app/email.html", {'title':'Confirmation mail', 'name':user['email']})
#         text_conte




# Defining employees function
def emp1(request):
    eq=Enquiry.objects.all()
    return render(request,'chat/emp1.html',{'eq':eq})


def chatemp1(request):
    return render(request,'chat/chatemp1.html')