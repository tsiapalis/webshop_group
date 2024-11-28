from django.urls import path
from . import views
from .discovery_view import Discovery

app_name = 'core_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('discovery/', Discovery.as_view(), name='discovery'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/success/', views.logout_success, name='logout_success'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('about/', views.about, name='about'),
    path('registration/', views.register, name='registration'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
