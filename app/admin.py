from django.contrib import admin
from .models import Enquiry


# Model style 
class EnquiryAdmin(admin.ModelAdmin):
  list_display =['name', 'phone','enquiry_no']
# Register your models here.
admin.site.register(Enquiry,EnquiryAdmin)
