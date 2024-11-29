from django.urls import path
from . import views
from . import auth_views
from .discovery_view import Discovery, SearchView
from .review_view import ReviewView
from .cart_view import CartView

app_name = 'core_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('discovery/', Discovery.as_view(), name='discovery'),
    path('search/', SearchView.as_view(), name='search'),
    path('cart/', CartView.as_view(), name='cart'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('review/', ReviewView.as_view(), name='review'),
    path('about/', views.about, name='about'),
    path('item/<int:item_id>', Discovery.as_view(), name='detailed_item'),
    path('registration/', auth_views.RegisterView.as_view(), name='registration'),
    path('reset-password/', auth_views.ResetPasswordView.as_view(), name='reset_password'),
]
