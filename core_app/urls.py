
from django.urls import path
from core_app import views

app_name = 'basic_app'

urlpatterns = [
    path('', views.index, name='index'),
]