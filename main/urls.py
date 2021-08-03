from os import name
from django.urls import path,include
from .views import *
urlpatterns = [
    path('', indexpage,name='home'),
    path('download', download_dataframe,name='download_dataframe'),
]