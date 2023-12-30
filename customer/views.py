# customer/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Customer, Image
from .forms import CustomerForm
from django.contrib import messages
from django.views.generic.detail import DetailView
from .forms import CustomerEditForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.views.generic import DetailView
# from xhtml2pdf import pisa
from django.db.models import Sum
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView



def index (request):
    return render(request, 'customer/index.html')

@login_required
def home(request):
    template_name = 'customer/home.html'
    customer_list = Customer.objects.all()

    # Calculate the total number of customers
    total_customers_count = customer_list.count()

    # Calculate the total sets collected for all customers
    total_sets = customer_list.aggregate(Sum('total_sets'))['total_sets__sum']

    def remove_sets_for_expired_customers():
    # Get the current date
        current_date = timezone.now().date()

    # Get customers whose status has passed the collection date
        expired_customers = Customer.objects.filter(status='Completed', sets__collection_date__lt=current_date)

    # Loop through expired customers and reset their total_sets field
        for customer in expired_customers:
            customer.total_sets = 0
            customer.save()


    # Configure pagination
    paginator = Paginator(customer_list, 5)
    page = request.GET.get('page')

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    recent_customers = Customer.objects.order_by('-date_of_register')[:4]
    passed_collection_count = customer_list.filter(date_of_collection__lt=timezone.now().date()).count()
    not_passed_collection_count = customer_list.filter(date_of_collection__gte=timezone.now().date()).count()

    current_datetime = timezone.now()

    context = {
        'recent_customers': recent_customers,
        'passed_collection_count': passed_collection_count,
        'not_passed_collection_count': not_passed_collection_count,
        'current_datetime': current_datetime,
        'total_customers_count': total_customers_count,
        'total_sets': total_sets,  # Pass the total sets to the template
        'customers': customers,
    }

    return render(request, template_name, context)

# Add the TotalSetsView function-based view as well
def total_sets_view(request):
    template_name = 'customer/total_sets.html'
    # Calculate the total sets collected for all customers
    total_sets = Customer.objects.aggregate(Sum('total_sets'))['total_sets__sum']

    context = {'total_sets': total_sets}
    return render(request, template_name, context)

@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form and handle the images accordingly
            customer = form.save()
            single_picture = form.cleaned_data['picture']
            multiple_pictures = request.FILES.getlist('multiple_pictures')

            # Save the single picture if provided
            if single_picture:
                Image.objects.create(customer=customer, picture=single_picture)

            # Save multiple pictures if provided
            for picture in multiple_pictures:
                Image.objects.create(customer=customer, picture=picture)

            return redirect('all_customers')
    else:
        form = CustomerForm()

    context = {'form': form}
    return render(request, 'customer/add_customer.html', context)

@login_required
def all_customers(request):
    query = request.GET.get('q')
    customers = Customer.objects.all()

    if query:
        customers = customers.filter(Q(name__icontains=query) | Q(phone__icontains=query))

     # Configure pagination
    paginator = Paginator(customers, 10)  # Show 10 customers per page
    page = request.GET.get('page')

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        customers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        customers = paginator.page(paginator.num_pages)

    current_datetime = timezone.now()

    # Fetch all customers
    all_customers = Customer.objects.all()

     # Calculate the total number of customers
    total_customers_count = all_customers.count()

    context = {
        'customers': customers, 
        'query': query, 
        'current_datetime': current_datetime,
        'total_customers_count': total_customers_count,
    }

    return render(request, 'customer/all_customers.html', context)


@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.method == 'POST':
        form = CustomerEditForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', pk=customer.id)
    else:
        form = CustomerEditForm(instance=customer)

    return render(request, 'customer/edit_customer.html', {'form': form, 'customer': customer})


class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'
    context_object_name = 'customer'


def search_customer(request):
    query = request.GET.get('q')
    customers = Customer.objects.all()

    if query:
        customers = customers.filter(Q(name__icontains=query) | Q(phone__icontains=query))

    return render(request, 'customer/all_customers.html', {'customers': customers, 'query': query})


class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customer/customer_confirm_delete.html'
    success_url = reverse_lazy('all_customers')


def total_amount_paid_view(request):
    total_amount_paid = Customer.objects.aggregate(Sum('amount_paid'))['amount_paid__sum']
    total_amount_paid = total_amount_paid or 0

    return render(request, 'customer/total_amount_paid.html', {'total_amount_paid': total_amount_paid})


