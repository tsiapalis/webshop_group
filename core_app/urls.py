from django.urls import path

from .views import views
from .views.auth_views import LoginView, RegisterView, ResetPasswordView, logout_view
from .views.discovery_view import Discovery
from .views.review_view import ReviewView
from .views.cart_view import CartView
from .views.checkout_view import DetailsView, ShippingView, PaymentView, PaymentConfirmedView
from .views.profile_view import InfoChangeView, BillingPayments, Settings, TransactionsHistory


app_name = 'core_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('discovery/', Discovery.as_view(), name='discovery'),
    path('item/<int:item_id>', Discovery.as_view(), name='detailed_item'),
    path('cart/', CartView.as_view(), name='cart'),
    # Auth Views
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('review/', ReviewView.as_view(), name='review'),
    path('about/', views.about, name='about'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    # Settings Views
    path('my-profile/', InfoChangeView.as_view(), name='my_profile'),
    path('my-profile/details', InfoChangeView.as_view(), name='details'),
    path('my-profile/transactions', TransactionsHistory.as_view(), name='transactions'),
    path('my-profile/billing', BillingPayments.as_view(), name='billing'),
    path('my-profile/settings', Settings.as_view(), name='settings'),
    # Checkout Views
    path('checkout/details', DetailsView.as_view(), name='checkout_details'),
    path('checkout/shipping', ShippingView.as_view(), name='checkout_shipping'),
    path('checkout/payment', PaymentView.as_view(), name='checkout_payment'),
    path('checkout/payment/confirmation/<int:order_number>/', PaymentConfirmedView.as_view(), name='payment_confirmed'),
]
