from django.shortcuts import redirect, render
from cart.models import CartItem
from .models import Order
from django.contrib.auth.decorators import login_required
import datetime
# Create your views here.

@login_required(login_url='login')
def place_order(request,total=0,grand_total=0):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('store')

    quantity=0

    for cart_item in cart_items:
        total=total+(cart_item.product.price*cart_item.quantity)
        quantity=quantity+cart_item.quantity
        tax=(8*total)/100
        grand_total=total+tax

    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        address_line_1=request.POST.get('address_line_1')
        address_line_2=request.POST.get('address_line_2')
        country=request.POST.get('country')
        state=request.POST.get('state')
        city=request.POST.get('city')
        order_note=request.POST.get('order_note')
        ip=request.META.get('REMOTE_ADDR')
        tax=tax
        user=current_user
        final_total=grand_total
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr,mt,dt)
        current_date = d.strftime("%Y%m%d") #20210305
        order_number = current_date + str(user.id)
        data=Order(user=user,first_name=first_name,last_name=last_name,email=email,phone=phone,address_line_1=address_line_1,address_line_2=address_line_2,country=country,state=state,city=city,order_note=order_note,tax=tax,ip=ip,order_total=final_total,order_number=order_number)
        data.save()
        order=Order.objects.filter(user=current_user,is_ordered=False,order_number=order_number).last()



        context={

                'cart_items':cart_items,
                'grand_total':grand_total,
                'tax':tax,
                'total':total,
                'quantity':quantity,
                'order':order
            }

        return render(request,'accounts/payment.html',context)
    else:
        return redirect('checkout')
