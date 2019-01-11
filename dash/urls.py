from django.urls import path,include
from django.conf.urls import url 
from . import views

# Add your URLs here

urlpatterns = [
    url('',views.dash_view,name='dash')
]