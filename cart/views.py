
from django.shortcuts import render,redirect,get_object_or_404
from matplotlib.style import context
from store.models import Variation
from store.models import Product
from django.contrib.auth.decorators import login_required

from store.models import Product
from .models import Cart, CartItem
# Create your views here.

def _cart_id(request):#Private Fucntion
    cart_id=request.session.session_key # Fetched Session Key
    if not cart_id:
        cart_id=request.session.create()
    return cart_id

def cart(request,total=0,quantity=0,tax=0,grand_total=0,cart_items=None):
    
    try:
        if request.user.is_authenticated:

            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
            for cart_item in cart_items:
                total=total+(cart_item.product.price*cart_item.quantity)
                quantity=quantity+cart_item.quantity
                tax=(total*8)/100
                grand_total=total+tax
            

        else:   
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart)
            
            for cart_item in cart_items:
                total=total+(cart_item.product.price*cart_item.quantity)
                quantity=quantity+cart_item.quantity
                tax=(total*8)/100
                grand_total=total+tax
                
        context={
                    'cart_items':cart_items,
                    'grand_total':grand_total,
                    'total':total,
                    'tax':tax,
                    'quantity':quantity,
                }

    except Exception as e:
                raise e

    return render(request,'store/cart.html',context)

        



  

    

def add_cart(request,product_id):
    current_user=request.user

    product=Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation=[]
        if request.method=="POST":
            for item in request.POST:
                key=item
                value=request.POST[key]
                #print(key,value)

                try:
                
                    
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                    print(product_variation)
                    # print(variation)    
                except:
                    pass

                    
            


       

        is_cart_item_exists=CartItem.objects.filter(product=product,user=current_user).exists()

        if is_cart_item_exists:

            cart_item=CartItem.objects.filter(product=product,user=current_user)
            exist_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                exist_var_list.append(list(existing_variation))
                
                id.append(item.id)

            if product_variation in exist_var_list:
                index=exist_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                
                item.save()
                # CartItem.objects.get(product=product)

            else:
                item=CartItem.objects.create(product=product,quantity=1,user=current_user)

                if len(product_variation)>0:
                
                        item.variation.add(*product_variation)

                item.save()
                # cart_item.quantity=cart_item.quantity+1
        
        else:
            cart_item=CartItem.objects.create(
                quantity=1,
                user=current_user,
                product=product
            )
            if len(product_variation)>0:
                
                    cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect ('cart')

    else:
         product=Product.objects.get(id=product_id)
    product_variation=[]
    if request.method=="POST":
        for item in request.POST:
            key=item
            value=request.POST[key]
            #print(key,value)

            try:
            
                
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
                print(product_variation)
                # print(variation)    
            except:
                pass

                
           


    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
       cart=Cart.objects.create(
           cart_id=_cart_id(request)
           )
    cart.save()

    is_cart_item_exists=CartItem.objects.filter(product=product,cart=cart).exists()

    if is_cart_item_exists:

        cart_item=CartItem.objects.filter(product=product,cart=cart)
        exist_var_list=[]
        id=[]
        for item in cart_item:
            existing_variation=item.variation.all()
            exist_var_list.append(list(existing_variation))
            
            id.append(item.id)

        if product_variation in exist_var_list:
            index=exist_var_list.index(product_variation)
            item_id=id[index]
            item=CartItem.objects.get(product=product,id=item_id)
            item.quantity+=1
            
            item.save()
            # CartItem.objects.get(product=product)

        else:
            item=CartItem.objects.create(product=product,quantity=1,cart=cart)

            if len(product_variation)>0:
            
                    item.variation.add(*product_variation)

            item.save()
            # cart_item.quantity=cart_item.quantity+1
    
    else:
        cart_item=CartItem.objects.create(
            quantity=1,
            cart=cart,
            product=product
        )
        if len(product_variation)>0:
            
                cart_item.variation.add(*product_variation)
        cart_item.save()
    return redirect ('cart')




def remove_cart(request,product_id,cart_item_id):
    try:
        
        product=get_object_or_404(Product,id=product_id)
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(user=request.user,product=product,id=cart_item_id)
            if cart_item.quantity>1:
                cart_item.quantity=cart_item.quantity-1
                cart_item.save()
            else:
                cart_item.delete()
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(cart=cart,product=product,id=cart_item_id)
            if cart_item.quantity>1:
                cart_item.quantity=cart_item.quantity-1
                cart_item.save()
            else:
                cart_item.delete()
    except:
            pass
    return redirect('cart')

def remove_cart_item(request,product_id,cart_item_id):
    try:
        product=get_object_or_404(Product,id=product_id)
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
            cart_item.delete()
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
            cart_item.delete()
    except:
        pass
    return redirect('cart')
    
    
@login_required(login_url='login')
def checkout(request):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
 


    context={
            'cart_items':cart_items,
            # 'grand_total':grand_total,
            # 'tax':tax,
            # 'total':total,
            # 'quantity':quantity,
    }

        
    return render(request,'store/checkout.html',context)