from django.contrib import admin
from .models import User,Product,InventoryTracking,RawMaterial,ReplacementAndRejection,MaterialMovementRecord
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name','last_name','email']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['status','name','arrival_date','dispatch_date',]

admin.site.register(InventoryTracking)
admin.site.register(ReplacementAndRejection)
admin.site.register(RawMaterial)
admin.site.register(MaterialMovementRecord)
