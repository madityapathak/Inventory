from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User,Product,RawMaterial,InventoryTracking
from django import forms

class UserForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['email','username','first_name','last_name']


class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields = [ 'status','name','arrival_date','dispatch_date','code' ]
        
        widgets = {
            'arrival_date': forms.DateInput(attrs={"class":"form-control",'type':'date'}),
            'dispatch_date': forms.DateInput(attrs={"class":"form-control",'type':'date'})
        }

class RawMaterialForm(ModelForm):
    class Meta:
        model=RawMaterial
        fields = ['name']


class InventoryManagementForm(ModelForm):
    class Meta:
        model=InventoryTracking
        fields = [ 'product','raw_material','quantity','added_to_inven_on' ]
        
        widgets = {
            'product': forms.Select(attrs={"class":"form-control"}),
            'raw_material': forms.Select(attrs={"class":"form-control"}),
            "added_to_inven_on" : forms.DateInput(attrs={"class":"form-control",'type':'date'}),
        }