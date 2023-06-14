from django.db import models

# Create your models here.
class Enquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    enquiry_details = models.TextField()
    enquiry_no=models.CharField(max_length=255,default="")
    quotation_no=models.CharField(max_length=255,default="")




    def __str__(self):
        return "{self.name}  {self.quotation_no}".format(self=self)

