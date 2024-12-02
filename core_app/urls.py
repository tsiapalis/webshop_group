from django.urls import path
from . import views
from . import auth_views, profile_view
from .discovery_view import Discovery
from .review_view import ReviewView

app_name = 'core_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('discovery/', Discovery.as_view(), name='discovery'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('review/', ReviewView.as_view(), name='review'),
    path('about/', views.about, name='about'),
    path('item/<int:item_id>', Discovery.as_view(), name='detailed_item'),
    path('registration/', auth_views.RegisterView.as_view(), name='registration'),
    path('reset-password/', auth_views.ResetPasswordView.as_view(), name='reset_password'),
    path('my-profile/', profile_view.InfoChangeView.as_view(), name='my_profile'),
    path('my-profile/details', profile_view.InfoChangeView.as_view(), name='details'),
    path('my-profile/transactions', profile_view.TransactionsHistory.as_view(), name='transactions'),
    path('my-profile/billing', profile_view.BillingPayments.as_view(), name='billing'),
    path('my-profile/settings', profile_view.Settings.as_view(), name='settings'),
]
