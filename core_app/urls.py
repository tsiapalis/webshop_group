from django.urls import path
from . import views

app_name = 'core_app'

urlpatterns = [

    path('', views.index, name='index'),
    path('discovery/', views.discovery, name='discovery'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logout/success/', views.logout_success, name='logout_success'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('about/', views.about, name='about'),
    path('registration/', views.register, name='registration')
]
