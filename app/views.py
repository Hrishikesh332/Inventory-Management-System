from django.shortcuts import render
import requests
from django.db import models
from django.core.mail import send_mail

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

# def main():
#     form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSfxutpV5s03otr0wEz_pytrBnW8f78LEj08YtFcKZ79mSf1fQ/viewform?usp=sf_link'
#     data = get_enquiry_data(form_url)
#     save_enquiry_data(data)
#     send_confirmation_email(data)
