from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator,MaxValueValidator, MinValueValidator
from django.core import validators
from home.models import Category



states_choices = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))
class SellerRegister(models.Model):
	name=models.CharField(max_length=100)
	mobile=models.IntegerField(default=None)
	email=models.EmailField()
	password=models.CharField(max_length=100,validators=[MinLengthValidator(8)])
	
	state=models.CharField(choices=states_choices,max_length=100,default=None)
	city=models.CharField(max_length=100,default=None)
	pincode=models.IntegerField(default=None)
	pickup_address=models.CharField(max_length=500)

	def __str__(self):
		return self.name

class SellerProduct(models.Model):
	name=models.CharField(max_length=200)
	category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
	price=models.IntegerField()
	dis_price=models.IntegerField()
	desc=models.CharField(max_length=500)
	image=models.ImageField(null=True,upload_to='images/')
	image1=models.ImageField(null=True,upload_to='images/')
	image2=models.ImageField(null=True,upload_to='images/')
	image3=models.ImageField(null=True,upload_to='images/')
	offer=models.BooleanField(default=False)
	date=models.DateField(auto_now_add=True)
	seller=models.ForeignKey(SellerRegister,on_delete=models.CASCADE,default=None)
	def __str__(self):
		return self.name