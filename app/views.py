from django.shortcuts import render
from django.db import models
from django.core.mail import send_mail
from .models import Enquiry
import uuid

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



def enquiry(request):
    return render(request,'enquiry.html')

def index(request):
    if request.method=='POST':
        enquiry=Enquiry()
        enquiry.name=request.POST.get('name')
        enquiry.email=request.POST.get('email')
        enquiry.phone=request.POST.get('phone')
        enquiry.enquiry_details=request.POST.get('enquiry_details')

        # Generate enquiry number
        enquiry_no = str(uuid.uuid4())
        # enquiry.enquiry_no = enquiry_no  

        quotation_no = str(uuid.uuid4())
        quotation_no = "QN-" + name[:3]+ quotation_no[:8]
        print(enquiry_no, quotation_no)

        enquiry.save()
        return render(request,'index.html')
    else:
        return render(request,'enquiry.html')


# def sendmail(id):

#     user=Enquirys.objects.all().values()

#     if (user['name']==True):
#         html_content = render_to_string("app/email.html", {'title':'Confirmation mail', 'name':user['email']})
#         text_conte