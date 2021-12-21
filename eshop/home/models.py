from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator,MaxValueValidator, MinValueValidator
from django.core import validators

# Create your models here.
class Category(models.Model):
	type=models.CharField(max_length=30)
	clas=models.CharField(max_length=30)
	def __str__(self):
		return self.type

state_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))
class Customers(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,default=None,null=True,blank=True)
	
	mobile=models.IntegerField()
	state=models.CharField(choices=state_choices,max_length=100,default=None)
	city=models.CharField(max_length=100,default=None)
	pincode=models.IntegerField(default=None)
	
	
	
			
class Product(models.Model):
	seller=models.ForeignKey("seller.SellerRegister",on_delete=models.CASCADE,default=None,null=True)
	name=models.CharField(max_length=200)
	category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
	price=models.IntegerField()
	dis_price=models.IntegerField(default=1)
	desc=models.CharField(max_length=500)
	image=models.ImageField(null=True,upload_to='images/')
	image1=models.ImageField(null=True,upload_to='images/')
	image2=models.ImageField(null=True,upload_to='images/')
	image3=models.ImageField(null=True,upload_to='images/')
	offer=models.BooleanField(default=False)
	date=models.DateField(auto_now_add=True)

	def __str__(self):
		return self.name



class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
	quantity=models.PositiveIntegerField(default=1,null=True,validators=[MinValueValidator(1)])
	total=models.IntegerField(default=1)
    
	def total_cost(self):
		return self.quantity * self.product.price

order_status=(('Pending','Pending'),('Accepted','Accepted'),('Packed','Packed'),('On the way','On the way'),('Delivered','Delivered'),('Canceled','Canceled'))
class Order(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,default=None,blank=True)
	seller=models.ForeignKey("seller.SellerRegister",on_delete=models.CASCADE,default=None,null=True)
	product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None,null=True,blank=True)
	quantity=models.IntegerField(default=0)
	amount=models.IntegerField(default=0)
	order_id=models.CharField(max_length=500,blank=True)
	status=models.CharField(choices=order_status,default=order_status[0][0],max_length=100,null=True)
	paid=models.BooleanField(max_length=500,blank=True)
	date=models.DateField(auto_now_add=True)
	

class Address(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True,blank=True)
	address=models.TextField(max_length=500)


class Review(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None,null=True,blank=True)
	user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,null=True,blank=True)
	review=models.CharField(max_length=500)
	date=models.DateField(auto_now_add=True)  

class Message(models.Model):
	name=models.CharField(max_length=50)
	email=models.CharField(max_length=50)
	subject=models.CharField(max_length=100)
	message=models.CharField(max_length=500)

class Transcation(models.Model):
	product=models.ForeignKey(Product,on_delete=models.CASCADE)
	amount=models.IntegerField(default=0)