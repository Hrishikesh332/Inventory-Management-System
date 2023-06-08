from django.db import models

# Create your models here.
class Enquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    enquiry_details = models.TextField()

