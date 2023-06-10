from django.contrib import admin
from django.urls import path,include
from .views import enquiry
from .views import index
from .views import emp

urlpatterns = [
    path('',index),
    path('enquiry',enquiry),
    path('emp',emp)
]