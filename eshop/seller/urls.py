from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('seller_home/',views.seller_home,name='seller_home'),
    path('seller_login/',views.seller_login,name='seller_login'),
    path('seller_register/',views.seller_register,name='seller_register'),
    path('seller_order/',views.seller_order,name='seller_order'),
    path('seller_product/',views.seller_product,name='seller_product'),
    path('vendor/',views.Vendor,name='vendor'),
    path('accept_order/<ac_id>/',views.accept_order,name='accept_order'),
    path('seller_page/',views.seller_page,name='seller_page'),
    path('profile/',views.profile,name='profile')
    ]