from django.urls import path
from . import views

app_name = 'core_app'

urlpatterns = [

    path('', views.index, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('about/', views.about, name='about'),
    path('registration/', views.register, name='registration')
]
