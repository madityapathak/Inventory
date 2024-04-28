from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import User,Product,InventoryTracking,MaterialMovementRecord,ReplacementAndRejection
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm,ProductForm,RawMaterialForm,InventoryManagementForm

# Create your views here.
def log_in(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
            except:
                messages.error(request, 'enter correct email')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request,user)
                return redirect('accounts:home')
            else:
                messages.error(request, 'enter correct password')
        else:
            messages.error(request, 'Enter valid email and pasword')
    return render(request,'accounts/login.html')

def sign_up(request):
    context={}
    context['UserForm']=UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)

        pass1=request.POST.get("password1")
        pass2=request.POST.get("password2")
        usrn=request.POST.get("username")
        mail=request.POST.get("email")
        try:
            usr_1=User.objects.get(email=mail)
        except:
            usr_1=False
        try:
            usr=User.objects.get(username=usrn)
        except:
            usr=False
                                                                                   
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('accounts:login')

        else:
            print(form.errors.as_json())
            messages.error(request, form.errors.as_json())
            if usr_1:
                messages.error(request, "email is taken")
            if pass1 == pass2 and len(pass1) <= 7 :
                messages.error(request, 'password too short')
            if usr:
                messages.error(request, 'username is taken')
            if pass1 != pass2:
                messages.error(request, 'passwords did not match')
            return redirect('accounts:signup')
    return render(request,"accounts/signup.html",context)


def log_out(request):
    logout(request)
    return redirect ('accounts:login')


@login_required(login_url='accounts:login')
def home(request):
    context={}
    products=Product.objects.all()
    context['products']=products
    return render(request, 'accounts/home.html',context)

@login_required(login_url='accounts:login')
def product_details(request,pk):
    context={}
    product=Product.objects.get(id=pk)
    context['product']=product
    return render(request, 'accounts/productdetails.html',context)


@login_required(login_url='accounts:login')
def add_product(request):
    context={}
    context['ProductForm']=ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('accounts:home')
    return render(request, 'accounts/addproduct.html',context)

@login_required(login_url='accounts:login')
def add_raw_material(request):
    context={}
    context['MaterialForm']=RawMaterialForm()
    if request.method == 'POST':
        form = RawMaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.save()
            return redirect('accounts:home')
    return render(request, 'accounts/addmaterial.html',context)



@login_required(login_url='accounts:login')
def add_item_in_inventory(request):
    context={}
    context['InventoryForm']=InventoryManagementForm()
    if request.method == 'POST':
        form = InventoryManagementForm(request.POST)
        if form.is_valid():
            if request.POST["product"]:
                try:
                    get_record = InventoryTracking.objects.get(product=request.POST["product"])
                except:
                    get_record = False
                if get_record:
                    quantity = int(get_record.quantity)+int(request.POST["quantity"])
                    get_record.quantity=quantity
                    if request.POST["added_to_inven_on"]:
                        get_record.added_to_inven_on=request.POST["added_to_inven_on"]
                    get_record.save()
                else:    
                    record = form.save(commit=False)
                    record.save()
            elif request.POST["raw_material"]:
                try:
                    get_record = InventoryTracking.objects.get(raw_material=request.POST["raw_material"])
                except:
                    get_record = False
                if get_record:
                    quantity = int(get_record.quantity)+int(request.POST["quantity"])
                    get_record.quantity=quantity
                    if request.POST["added_to_inven_on"]:
                        get_record.added_to_inven_on=request.POST["added_to_inven_on"]
                    get_record.save()
                else:    
                    record = form.save(commit=False)
                    record.save()
            return redirect('accounts:inventory')
    return render(request, 'accounts/addinventoryrecord.html',context)

@login_required(login_url='accounts:login')
def repair_and_reject(request):
    context={}
    products = ReplacementAndRejection.objects.all()
    context['products']=products
    return render(request, 'accounts/repairandrejection.html',context)

from django.db.models import F
@login_required(login_url='accounts:login')
def inventory(request):
    context={}
    details = InventoryTracking.objects.select_related('product', 'raw_material__material_movement').annotate(stage=F('raw_material__material_movement__stage'),material_status=F('raw_material__material_movement__material_status'))
    context['details']=details
    return render(request, 'accounts/inventory.html',context)