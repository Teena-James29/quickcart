from django import forms
from .models import Product,Profile

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        exclude=['us']
        # fields='__all__'

class Profileform(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['us']




