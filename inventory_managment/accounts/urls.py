from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
   
    path('login/', views.log_in ,name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('',views.home,name='home'),
    path('logout/', views.log_out ,name='logout'),


    
    path('productdetails/<str:pk>/',views.product_details,name="productdetail"),
    path('addproduct/',views.add_product,name="addproduct"),
    path('addrawmaterial/',views.add_raw_material,name="addrawmaterial"),


    path('inventory/',views.inventory,name="inventory"),
    path('addinventoryitem/',views.add_item_in_inventory,name="additemininventory"),
    path('repairandreject/',views.repair_and_reject,name="repairandreject"),
]