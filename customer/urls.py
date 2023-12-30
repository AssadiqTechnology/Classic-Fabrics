# customer/urls.py
from django.urls import path
from .views import home, add_customer, search_customer, edit_customer, all_customers, index, CustomerDeleteView, total_amount_paid_view, CustomerDetailView  # Remove the problematic import

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('add/', add_customer, name='add_customer'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('search/', search_customer, name='search_customer'),
    path('all_customers/', all_customers, name='all_customers'),
    path('edit/<int:customer_id>/', edit_customer, name='edit_customer'),
    path('<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),
    path('total-amount-paid/', total_amount_paid_view, name='total_amount_paid'),
    # Add other URL patterns for your app as needed
]
