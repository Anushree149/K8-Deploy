
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate
from store.models import Product

def home(request):
    products= Product.objects.all().filter(is_available=True)
    product_count=products.count()
   
    context={
    'products':products,
    'product_count':product_count,
   }

    return render(request,'home.html',context)
    



    