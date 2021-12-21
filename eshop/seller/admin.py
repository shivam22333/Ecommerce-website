from django.contrib import admin
from seller.models import SellerProduct,SellerRegister
# Register your models here.
@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
	list_display=('id','name','category','price','offer')

@admin.register(SellerRegister)
class SellerRegisterAdmin(admin.ModelAdmin):
	list_display=('id','name','email')