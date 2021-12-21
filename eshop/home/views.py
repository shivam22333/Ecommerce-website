from home.models import Product,Customers,Category,Cart,Address,Order,Review,Message,Transcation
from seller.models import SellerRegister
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.db import connection
from .forms import RegisterForm,VendorForm,LoginForm,Profile,AddressForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.db.models import Q
import operator
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    l=Category.objects.all()
    s=Product.objects.filter(category=1)
    m=Product.objects.order_by('date')[:10]
    try:
        usr=request.user
        cart=Cart.objects.filter(user=usr)
        a=len(cart)
        return render(request,'index.html',{'l':l,'s':s,'a':a,'date':m})
    except:
        return render(request,'index.html',{'l':l,'s':s,'date':m})


def addcart(request,c_id):
    user=request.user
    product=Product.objects.get(id=c_id)
    # try:
    #     f=Cart.objects.get(product=product)
    #     q=f.quantity+1
    #     Cart(id=f.id,user=f.user,product=f.product,quantity=q).save()
    # except:
    total=product.price  
    Cart(user=user,product=product,total=total).save()
    return redirect('detail',my_id=c_id)

def showcart(request):
    if request.user.is_authenticated:
        usr=request.user
        cart=Cart.objects.filter(user=usr)
        a=len(cart)
        t=0
        s=0
        f=0
        
        #total=cart.product.price * cart.quantity
        # Cart(user=usr,product=cart.product,total=total).save()
        if cart:
            for p in Cart.objects.filter(user=usr) :
                
                t+=p.total #sub total
            if t<600:
                s=70 #shipping
                f=s+t # grand total
            else:
                s=0
                f=s+t
        return render(request,'cart.html',{'cart':cart,'t':t,'f':f,'s':s,'a':a})
    else:
        return render(request,'show.html')


def removecart(request,r_id):
    f=Cart.objects.get(id=r_id)
    f.delete()
    return redirect('showcart')


def plus(request,p_id):
    s=Cart.objects.get(id=p_id)
    f=s.quantity+1
    #total=s.total+s.product.price
    t=f*s.product.price
    Cart(id=s.id,user=s.user,product=s.product,quantity=f,total=t).save()
    return redirect('showcart')


def minus(request,m_id):
    s=Cart.objects.get(id=m_id)
    f=s.quantity-1
    if f>=1:
        t=f*s.product.price
        Cart(id=s.id,user=s.user,product=s.product,quantity=f,total=t).save()
    else:
        return redirect('remove',r_id=s.id)
    return redirect('showcart')

def product(request,id):
    items=Product.objects.filter(category=id)

    try:
        usr=request.user
        cart=Cart.objects.filter(user=usr)
        a=len(cart)
        return render(request,'1.html',{'items':items,'id':id,'a':a})
    #items=Product.objects.filter(category='cloth',price__lte=21)
    #items=Product.objects.order_by('price') ascend
    #items=Product.objects.order_by('-price') descend
    except:
        return render(request,'1.html',{'items':items,'id':id})

def detail(request,my_id):
    form=Product.objects.get(id=my_id)
    l=Product.objects.filter(category=form.category.id).exclude(id=my_id)
    r=Review.objects.filter(product=form)
    #go to cart or add cart (condition)
    try:
        s=Cart.objects.get(product=form) 
        try:
            usr=request.user
            cart=Cart.objects.filter(user=usr)
            a=len(cart)
            m=len(r)
            return render(request,'product-detail.html',{'form':form,'l':l,'s':s,'a':a,'r':r,'m':m})
        except:
            m=len(r)
            return render(request,'product-detail.html',{'form':form,'l':l,'s':s,'r':r,'m':m})

    except:
        try:
            usr=request.user
            cart=Cart.objects.filter(user=usr)
            a=len(cart)
            m=len(r)
            return render(request,'product-detail.html',{'form':form,'l':l,'a':a,'r':r,'m':m})
        except:
            m=len(r)
            return render(request,'product-detail.html',{'form':form,'l':l,'r':r,'m':m})
        

def checkout(request):
    if request.method=='POST':

        user=request.user
        c=Cart.objects.filter(user=user)
        
        a=len(c)
        total=0
        s=0
        f=0
        if c:
            for p in c:
                total+=p.total
            if total<=600:
                s=70
                f=total+s
            else:
                s=0
                f=total+s
        try:
            ad=request.POST['address']
            add=Address.objects.get(id=ad)
            return render(request,'checkout.html',{'total':total,'s':s,'f':f,'a':a,'cart':c,'add':add,'ad':ad})
        except:
             b=Address.objects.filter(user=user)
             error="Select anyone address"
             return render(request,'checkout.html',{'total':total,'s':s,'f':f,'a':a,'cart':c,'b':b,'error':error})
        
    else:
        user=request.user
        c=Cart.objects.filter(user=user)
        
        a=len(c)
        total=0
        s=0
        f=0
        if c:
            for p in c:
                total+=p.total
            if total<=600:
                s=70
                f=total+s
            else:
                s=0
                f=total+s
        b=Address.objects.filter(user=user)
        return render(request,'checkout.html',{'total':total,'s':s,'f':f,'a':a,'cart':c,'b':b})


def wishlist(request):
    return render(request,'wishlist.html')
# def register(request):
#     if request.method=='POST':
#         form=RegisterForm(request.POST)
#         if form.is_valid():
#             first=form.cleaned_data['first_name']
#             last=form.cleaned_data['last_name']
#             mobile=form.cleaned_data['mobile']
#             email=form.cleaned_data['email']
#             password=form.cleaned_data['password']
#             s=Customer.objects.filter(email=email)
#             if s:
#                 error_message='Email Already Taken'
#                 return render(request,'register.html',{'form':form,'error':error_message})
#             else:
#                 s=Customer.objects.filter(first_name=first,last_name=last,mobile=mobile,email=email,password=password)
#                 s.save()
#                 form=RegisterForm()
#                 return HttpResponseRedirect('/login')
#     else:
#         form=RegisterForm()

#     return render(request,'register.html',{'form':form})
# def login(request):
#     if request.method=='POST':
#         l=LoginForm(request.POST)
#         if l.is_valid():
#             email=l.cleaned_data['email']
#             password=l.cleaned_data['password']
#             s=Customer.objects.filter(email=email,password=password)
#             if s:
#                 error_message='Verification Success'
#                 return render(request,'login.html',{'fm':l,'error':error_message,'s':s})
#             else:
#                 error_message='Invalid Email/Password'
#                 return render(request,'login.html',{'fm':l,'error':error_message})
#     else:
#         l=LoginForm()
#     return render(request,'login.html',{'fm':l})
@csrf_exempt
def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        profile_form=Profile(request.POST)
        if form.is_valid() and profile_form.is_valid():
            email=form.cleaned_data['email']
            username=form.cleaned_data['username']
            s=User.objects.filter(email=email)

            if s:
                error_message='Email Already Taken'
                return render(request,'register.html',{'form':form,'profile':profile_form, 'error':error_message})
            else:
                user=form.save()
                profile=profile_form.save(commit=False)
                profile.user=user
                profile.save()
                form=RegisterForm()
                profile_form=Profile()
                
                
                html_content=render_to_string('email_registeration.html')
                text_content=strip_tags(html_content)
                
                subject="Registeration Successfull!!"
               
                send_mail(subject, text_content, 'arjunreddy2907@gmail.com',
                         [email], fail_silently=False, html_message=html_content)
                return redirect('login')
    else:
         form=RegisterForm()  
         profile_form=Profile()      
    return render(request,'register.html',{'form':form,'profile':profile_form})

@csrf_exempt
def login_user(request):
    
    
    if request.method=='POST':
        l=LoginForm(request.POST)
        if l.is_valid():
            username=l.cleaned_data['username']
            password=l.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                #messages.success(request,'success')
                return redirect('index')
            else:
                error_message='Invalid Username/Password'
                return render(request,'login.html',{'fm':l,'error':error_message})
    else:
        l=LoginForm()
    return render(request,'login.html',{'fm':l})    

def logout_user(request):
    logout(request)
    return redirect('index') 

def change(request):
    if request.method=='POST':
        l=PasswordChangeForm(user=request.user,data=request.POST)
        if l.is_valid():
            l.save()
            update_session_auth_hash(request,l.user)
            return redirect('index')
    else:
        l=PasswordChangeForm(user=request.user)
        return render(request,'change.html',{'l':l})

# def profile(request):
#     if request.method=='POST':
#         form=Profile(request.POST)
#         if form.is_valid():

#             u=request.user
#             mobile=form.cleaned_data['mobile']
#             address=form.cleaned_data['address_1']
#             address2=form.cleaned_data['address_2']
#             state=form.cleaned_data['state']
#             city=form.cleaned_data['city']
#             pincode=form.cleaned_data['pincode']
            
#             try:
#                 c=Customers.objects.get(user=u)
                
#                 f=Customers(id=c.id,user=u,mobile=mobile,address_1=address,address_2=address2,state=state,city=city,pincode=pincode)
#                 f.save()
#                 redirect('index')
#             except:
#                 f=Customers(user=u,mobile=mobile,address=address,state=state,city=city,pincode=pincode)
#                 f.save()
#                 redirect('index')

#     else:
        
#         form=Profile()
#     usr=request.user
#     cart=Cart.objects.filter(user=usr)
#     a=len(cart)
#     return render(request,'profile.html',{'form':form,'a':a})
def contact(request):
    try:
        usr=request.user
        cart=Cart.objects.filter(user=usr)
        a=len(cart)
        return render(request,'contact.html',{'a':a})
    except:
        return render(request,'contact.html')


def account(request):
    user=request.user
    s=Customers.objects.filter(user=user)
   
    cart=Cart.objects.filter(user=user)
    a=len(cart)
    address=AddressForm()
    b=Address.objects.filter(user=user)
    c=Order.objects.filter(user=user)
    return render(request,'my-account.html',{'name':request.user.get_full_name,'username':request.user.username,'email':request.user.email,'s':s,'a':a,'b':b,'address':address,'c':c})

def address(request):
    if request.method=='POST':
        address=AddressForm(request.POST)
        if address.is_valid():
            a=address.cleaned_data['address']
            s=Address(user=request.user,address=a)
            s.save()
            
            return redirect('account')
    else:
        address=AddressForm()

    b=Address.objects.filter(user=request.user)
    return render(request,'my-account.html',{'address':address,'b':b})

def edit_address(request,e_id):
    Address.objects.get(id=e_id).delete()
    return redirect('account')


def pay(request,f):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = int(f)*100
       #print(amount)
        #type(f)
        order_currency="INR"
        client = razorpay.Client(auth=("rzp_test_OOdnA7baC4aYyS", "yeOqEDouTEIFDOigL9aNN1vW")) #create razor client
        payment = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'})
        return render(request, 'pay.html',{'payment':payment})
    return render(request, 'pay.html')
@csrf_exempt
def success(request):
    if request.method=='POST':
        a=request.POST
        order_id=""
        for key,val in a.items():
            if key=='razorpay_payment_id':
                order_id=val
                break
        
        c=Cart.objects.filter(user=request.user)
        for ord in c:
            m=ord.product.seller
            Order.objects.create(seller=ord.product.seller,user=ord.user,product=ord.product,quantity=ord.quantity,amount=ord.total,order_id=order_id,paid=True)
            Transcation.objects.create(product=ord.product,amount=ord.total)
            ord.delete()
        return redirect('email_transaction')
    else:
        return render(request, "success.html")

def buy(request,f):
    user=request.user
    product=Product.objects.get(id=f)
    total=product.price  
    s=Cart.objects.filter(product=product)
    if s:
       
        return redirect('showcart')
    else:
        Cart(user=user,product=product,total=total).save()
        return redirect('showcart')

def check(request,pd_id):
    if request.method=='POST':

        user=request.user
        c=Cart.objects.get(product=pd_id)
        
        
        total=c.product.price*c.quantity
        s=0
        f=0
        if c:
            if total<=600:
                s=70
                f=total+s
            else:
                s=0
                f=total+s
        try:
            ad=request.POST['address']
            add=Address.objects.get(id=ad)
            return render(request,'check.html',{'total':total,'s':s,'f':f,'cart':c,'add':add,'ad':ad,'pd_id':pd_id})
        except:
             b=Address.objects.filter(user=user)
             error="Select anyone address"
             return render(request,'check.html',{'total':total,'s':s,'f':f,'a':a,'cart':c,'b':b,'error':error,'pd_id':pd_id})
        
    else:
        user=request.user
        c=Cart.objects.get(product=pd_id)
        
        
        total=0
        s=0
        f=0
        if c:
            
            total=c.product.price*c.quantity
            if total<=600:
                s=70
                f=total+s
            else:
                s=0
                f=total+s
        b=Address.objects.filter(user=user)
        return render(request,'check.html',{'total':total,'s':s,'f':f,'cart':c,'b':b,'pd_id':pd_id})



def review(request,re_id):
    
    
    if request.method=='POST':
        user=request.user
        if user.is_authenticated:    
            product=Product.objects.get(id=re_id)
            review=request.POST.get('Review')
            Review(user=request.user,product=product,review=review).save()
            return redirect('detail',my_id=re_id)
        else:
            product=Product.objects.get(id=re_id)
            error_message='Login Required!!'
            return redirect('detail',my_id=re_id)
    
    
def message(request):
    if request.method=='POST':
        name=request.POST.get('name')

        email=request.POST.get('email')
        
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        
        Message(name=name,email=email,subject=subject,message=message).save()
        # send_mail(subject,message ,email,['ecommshop637@gmail.com'])
        return redirect('contact')
    else:
        return redirect('contact')


def email_transaction(request):
    c=Transcation.objects.all()
    html_content=render_to_string('email.html',{'c':c,'user':request.user})
    text_content=strip_tags(html_content)
    user=request.user
    b=User.objects.get(username=user)
    print(b.email)
    to=b.email
    subject="Order Placed!!"
   
    send_mail(subject, text_content, 'ecommshop637@gmail.com',[to], fail_silently=False, html_message=html_content)
    
    Transcation.objects.all().delete()
    return redirect('success')


def search(request):
    if request.method=='POST':
        s=request.POST.get('search')
        m=Product.objects.filter(desc__contains=s) | Product.objects.filter(name__contains=s)
        if len(m)==0 :
            return render(request,'search.html')
        return render(request,'search.html',{'m':m,'s':s})
    else:
        return redirect('/')


def Cash(request):
    c=Cart.objects.filter(user=request.user)
    for ord in c:
        m=ord.product.seller
        Order.objects.create(seller=ord.product.seller,user=ord.user,product=ord.product,quantity=ord.quantity,amount=ord.total,paid=False)
        Transcation.objects.create(product=ord.product,amount=ord.total)
        ord.delete()
    return redirect('Order')

def Oder(request):
    c=Transcation.objects.all()
    html_content=render_to_string('email.html',{'c':c,'user':request.user})
    text_content=strip_tags(html_content)
    user=request.user
    b=User.objects.get(username=user)
    to=b.email
    subject="Order Placed!!"
   
    send_mail(subject, text_content, 'ecommshop637@gmail.com',
             [to], fail_silently=False, html_message=html_content)
    
    Transcation.objects.all().delete()
    return render(request,'cash.html')
