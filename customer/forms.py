# customer/forms.py
from django import forms
from .models import Customer, Image
from multiupload.fields import MultiFileField
from django.forms.widgets import DateInput

class CustomerForm(forms.ModelForm):
    picture = forms.ImageField(label='Single Picture', required=False)
    multiple_pictures = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5, label='Multiple Pictures', required=False)

    class Meta:
        model = Customer
        fields = '__all__'  # Include all fields from the Customer model

        widgets = {
            'date_of_collection': DateInput(attrs={'type': 'date'}),
            'date_of_register': DateInput(attrs={'type': 'date'}),
            # ... (other fields)
        }

        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['picture', 'pictures']

class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

        widgets = {
            'shoulder': forms.TextInput(attrs={'class': 'form-control'}),
            'sleeve': forms.TextInput(attrs={'class': 'form-control'}),
            'armhole': forms.TextInput(attrs={'class': 'form-control'}),
            'biceps': forms.TextInput(attrs={'class': 'form-control'}),
            'wrist': forms.TextInput(attrs={'class': 'form-control'}),
            'bust': forms.TextInput(attrs={'class': 'form-control'}),
            'shirt_length': forms.TextInput(attrs={'class': 'form-control'}),
            'waist': forms.TextInput(attrs={'class': 'form-control'}),
            'lap': forms.TextInput(attrs={'class': 'form-control'}),
            'stamina': forms.TextInput(attrs={'class': 'form-control'}),
            'ankle': forms.TextInput(attrs={'class': 'form-control'}),
            'neck': forms.TextInput(attrs={'class': 'form-control'}),
            'links': forms.TextInput(attrs={'class': 'form-control'}),
            'freehand': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_charged': forms.TextInput(attrs={'class': 'form-control'}),
            'amount_paid': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date_of_collection': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'picture': forms.FileInput(attrs={'class': 'form-control-file'}),
            'date_of_register': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
