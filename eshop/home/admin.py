from django.contrib import admin
from .models import Product,Category,Customers,Cart,Order,Address,Review,Message,Transcation
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display=('id','name','category','price','offer')

@admin.register(Customers)
class CustomerAdmin(admin.ModelAdmin):
  	list_display=('id','user','mobile','state','city','pincode')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display=('id','type')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	list_display=('id','user','product','quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display=('user','product','quantity','status','date')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
	list_display=('id','user','address')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display=('user','product')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display=('name','email')

@admin.register(Transcation)
class TranscationAdmin(admin.ModelAdmin):
	list_display=('product','amount')