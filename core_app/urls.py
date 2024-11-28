from django.urls import path
from . import views
from . import auth_views
from .discovery_view import Discovery

app_name = 'core_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('discovery/', Discovery.as_view(), name='discovery'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('logout/success/', auth_views.logout_success, name='logout_success'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('about/', views.about, name='about'),
    path('registration/', auth_views.register, name='registration'),
    path('reset-password/', auth_views.reset_password, name='reset_password'),
]
