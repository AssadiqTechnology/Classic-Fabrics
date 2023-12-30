from django.contrib import admin
from .models import Customer, Image
from .forms import CustomerForm

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class CustomerAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    form = CustomerForm  # Make sure to use your custom form here

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Image)