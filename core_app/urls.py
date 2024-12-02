from django.urls import path

from .views import views, profile_view
from .views.auth_views import LoginView, RegisterView, ResetPasswordView, logout_view
from .views.discovery_view import Discovery
from .views.review_view import ReviewView
from .views.cart_view import CartView

app_name = 'core_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('discovery/', Discovery.as_view(), name='discovery'),
    path('cart/', CartView.as_view(), name='cart'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('review/', ReviewView.as_view(), name='review'),
    path('about/', views.about, name='about'),
    path('item/<int:item_id>', Discovery.as_view(), name='detailed_item'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('my-profile/', profile_view.InfoChangeView.as_view(), name='my_profile'),
    path('my-profile/details', profile_view.InfoChangeView.as_view(), name='details'),
    path('my-profile/transactions', profile_view.TransactionsHistory.as_view(), name='transactions'),
    path('my-profile/billing', profile_view.BillingPayments.as_view(), name='billing'),
    path('my-profile/settings', profile_view.Settings.as_view(), name='settings'),
]
