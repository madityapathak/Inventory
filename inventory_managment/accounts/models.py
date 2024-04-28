from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']



class ProductStatusChoices(models.TextChoices):
        PACKED = 'Packed',
        DISPACHED = 'Dispached',
   
class Product(models.Model):
    status =  models.CharField(max_length=30, choices= ProductStatusChoices.choices)
    code = models.CharField(max_length=30,null=False,blank=False,unique=True)
    name = models.CharField(max_length=30,null=True,blank=True)
    arrival_date = models.DateTimeField(null=True,blank=True)
    dispatch_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return str(self.code)+"-"+str(self.name)
   
class RawMaterial(models.Model):
    name = models.CharField(max_length=30,null=True,blank=True)
    
    def __str__(self):
        return self.name

class InventoryTracking(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    added_to_inven_on = models.DateTimeField(null=True,blank=True)

class ReplacementAndRejection(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_in_repair=models.BooleanField(default=False,null=False)
    is_rejected=models.BooleanField(default=False,null=False)
    rejection_date = models.DateTimeField(null=True,blank=True)
    repair_completion_date =  models.DateTimeField(null=True,blank=True)



class MaterialMovementRecord(models.Model):
    material = models.OneToOneField(RawMaterial, on_delete=models.CASCADE,related_name='material_movement')
    stage = models.CharField(max_length=30,null=True,blank=True)
    material_status = models.CharField(max_length=30,null=True,blank=True)
    
    