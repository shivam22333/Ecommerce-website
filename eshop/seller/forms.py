from django import forms
from django.core import validators
from .models import SellerRegister
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class SellerRegisterForm(forms.ModelForm):
	retype_password=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
	class Meta:
 		model=SellerRegister
 		fields=['name','mobile','email','state','city','pincode','pickup_address','password']
 		labels={'retype_password':'Password(again)'}
 		help_text={'first_name':'Enter Your Name'}
 		widgets={'name':forms.TextInput(attrs={'class':'form-control form-control-sm',
 		'placeholder':'Enter Full Name'}),
 		'mobile':forms.TextInput(attrs={'class':'form-control form-control-sm',
 		'placeholder':'Mobile No'}),
 		'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}),
 		'password':forms.PasswordInput(attrs={'class':'form-control form-control-sm',
         'placeholder':'Enter Your Password'}),
 		'retype_password':forms.PasswordInput(attrs={'class':'form-control form-control-sm',
         'placeholder':'Enter Your Password again'}),
 		'state':forms.Select(attrs={'class':'form-control'}),
		'city':forms.TextInput(attrs={'class':'form-control form-control-sm',
		'placeholder':'City'}),
		'pincode':forms.NumberInput(attrs={'class':'form-control form-control-sm',
		'placeholder':'Pincode'}),
		'pickup_address':forms.TextInput(attrs={'class':'form-control form-control-sm',
		'placeholder':'Address'}),
 		}
	def clean(self):
 		cleaned_data=super().clean()
 		val1=self.cleaned_data['password']
 		val2=self.cleaned_data['retype_password']
 		if val1!=val2:
 			raise forms.ValidationError('Password not matched')


class SellerLoginForm(forms.ModelForm):
 	class Meta:
 		model=SellerRegister
 		fields=['email','password']
 		widgets={'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter Your Email'}),
 		'password':forms.PasswordInput(attrs={'class':'form-control',
         'placeholder':'Enter Your Password'}),
		
 		}
		