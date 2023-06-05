import imp
from multiprocessing import context
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from category.models import Category
from .models import Product
# Create your views here.
def store(request,category_slug=None):
    categories=None
    product=None

    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug) 
        product=Product.objects.filter(category=categories) #(Table name , Colmn name)
        paginator=Paginator(product,1)#No. of products per page
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)




        product_count=product.count()
        

    else:
        
        product=Product.objects.all().filter(is_available=True)
        paginator=Paginator(product,2)#No. of products per page
        page=request.GET.get('page')
        paged_products=paginator.get_page(page)
        product_count=product.count()
        
    context={
        'product': paged_products,       #Key : Value form
        'product_count':product_count,
        }

    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    try:
     single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
    except Exception as e:
        raise e

    context={
        'single_product':single_product
    }

    return render(request,'store/product_details.html',context)


def search(request):
    if 'keyword'in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            product=Product.objects.order_by('-created_at').filter(Q(desc__icontains=keyword)| Q(product_name__icontains=keyword))
            product_count=product.count()
        
            
    context={
        'product': product,       #Key : Value form
        'product_count':product_count,
        }
    return render (request,'store/store.html',context)