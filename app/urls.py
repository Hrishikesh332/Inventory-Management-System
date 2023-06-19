from django.contrib import admin
from django.urls import path,include
from .views import enquiry
from .views import index
from .views import emp1
from .views import chatemp1



urlpatterns = [
    path('',index),
    path('enquiry',enquiry),
    path('emp1',emp1),
    path('chatemp1',chatemp1)
]