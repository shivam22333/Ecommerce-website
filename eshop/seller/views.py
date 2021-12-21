from django.shortcuts import render,redirect
from seller.models import SellerRegister,User
from .forms import SellerRegisterForm,SellerLoginForm
from home.forms import VendorForm
from home.models import Order,Product,Category
from django.contrib.auth.hashers import make_password,check_password
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def seller_home(request):
    
    return render(request,'seller_home.html')


def seller_page(request):
    return render(request,'seller_page.html')


def Vendor(request):
    if request.method=='POST':
        lm=VendorForm(request.POST,request.FILES)
        if lm.is_valid():
            name=lm.cleaned_data['name']
            category=lm.cleaned_data['category']
            price=lm.cleaned_data['price']
            dis_price=lm.cleaned_data['dis_price']
            desc=lm.cleaned_data['desc']
            image=lm.cleaned_data['image']
            image1=lm.cleaned_data['image1']
            image2=lm.cleaned_data['image2']
            image3=lm.cleaned_data['image3']
            #offer=lm.cleaned_data['offer']
            
            a=SellerRegister.objects.get(id=request.session['seller'])
         
            s=Product.objects.create(seller=a,name=name,category=category,price=price,dis_price=dis_price,desc=desc,image=image,image1=image1,image2=image2,image3=image3)
            return redirect('vendor')
            #s.save()
            #return HttpResponseRedirect('/product')
        else:
            return redirect('vendor')
    else:
        lm=VendorForm()
        return render(request,'vendor.html',{'lm':lm})

def seller_order(request):
    m=SellerRegister.objects.get(id=request.session['seller'])
    a=Order.objects.filter(seller=m)
    
    return render(request,'seller_order.html',{'a':a})

def accept_order(request,ac_id):
    a=Order.objects.get(id=ac_id)
    m=User.objects.get(username=a.user)
    b=SellerRegister.objects.get(id=request.session['seller'])
    Order(id=ac_id,user=m,seller=b,product=a.product,quantity=a.quantity,amount=a.amount,status="Accepted",date=a.date,paid=a.paid).save()
    return redirect('seller_order')

@csrf_exempt
def seller_register(request):
    if request.method=='POST':
        a=SellerRegisterForm(request.POST)
        if a.is_valid():
            name=a.cleaned_data['name']
            mobile=a.cleaned_data['mobile']
            email=a.cleaned_data['email']
            password=a.cleaned_data['password']
            retype_password=a.cleaned_data['retype_password']
            state=a.cleaned_data['state']
            city=a.cleaned_data['city']
            pincode=a.cleaned_data['pincode']
            pickup_address=a.cleaned_data['pickup_address']
            if password!=retype_password:
                error_message="Password not matched"
                return render(request,'seller_register',{'fm':a,'error':error_message})
            try:
                f=SellerRegister.objects.get(email=email)
                error_message="Email Already Taken"
                return render(request,'seller_register.html',{'error':error_message,'fm':a})
            except:
                password=make_password(password)
                s=SellerRegister(name=name,mobile=mobile,email=email,password=password,state=state,city=city,pincode=pincode,pickup_address=pickup_address)
                s.save()
                return redirect('seller_home')
        else:
            error_message="Enter Valid Inputs"
            return render(request,'seller_register.html',{'error':error_message,'fm':a})
    else:
        a=SellerRegisterForm()
        return render(request,'seller_register.html',{'fm':a})

@csrf_exempt
def seller_login(request):
    if request.method=='POST':
        a=SellerLoginForm(request.POST)
        if a.is_valid():
            email=a.cleaned_data['email']
            password=a.cleaned_data['password']
            try:
                s=SellerRegister.objects.get(email=email)
                check=check_password(password,s.password)
                if check:
                    request.session['seller']=s.id
                    return redirect('seller_page')
                else:
                    error_message="Password Not Matched"
                    return render(request,'seller_login.html',{'fm':a,'error':error_message})
            except:
                error_message="Invalid Username/Password"
                return render(request,'seller_login.html',{'fm':a,'error':error_message})
        
    else:
        a=SellerLoginForm()
        return render(request,'seller_login.html',{'fm':a})


def seller_product(request):
     m=SellerRegister.objects.get(id=request.session['seller'])
     n=Category.objects.get(id=1)
     s=Product.objects.filter(seller=m,category=n)
     n1=Category.objects.get(id=2)
     s1=Product.objects.filter(seller=m,category=n1)
     n2=Category.objects.get(id=3)
     s2=Product.objects.filter(seller=m,category=n2)
     
     return render(request,'seller_product.html',{'s':s,'s1':s1,'s2':s2})

def profile(request):
     m=SellerRegister.objects.get(id=request.session['seller'])
     return render(request,'profile.html',{'m':m})