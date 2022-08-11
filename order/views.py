import datetime
from django.shortcuts import render,redirect

from carts.models import CartItem
from .models import Order
from .forms import OrderForm
from order.models import Order, OrderProduct, Payment
from store.models import Product
import razorpay
from django.conf import settings
from django.http import JsonResponse
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['order_number'])
    print(body)
    payment = Payment(
        user = request.user,
        payment_id = body['razorpay_payment_id'],
        amount_paid = body['amount_paid'],
        status = body['status'],
        payment_method = body['payment_method']
    )
    payment.save()
    order.payment = payment 
    order.is_ordered = True
    order.save()
    
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.Variation.set(product_variation)
        orderproduct.save()

        #reduce the quantity of sold product
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    #clear cart
    CartItem.objects.filter(user=request.user).delete()

    #send order recieved email
    mail_subject = 'Thank You. Your order has been recieved'
    message = render_to_string('order_recieved_email.html',{
        'user':request.user,
        'order':order,
        # 'domain':current_site,
        # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        # 'token':default_token_generator.make_token(user)
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


    data = {
        'order_number': order.order_number,
        'payment_id': payment.payment_id,
    }
    return JsonResponse(data)
    

def place_order(request, total=0, quantity=0):
    current_user=request.user

    #if cart_Item =0 rediret to store
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('store')
    #total=0
    for cart_item in cart_items:
        total +=(cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    if request.method=="POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            #store the all billing data in the order table  
            data=Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.phone=form.cleaned_data['phone']
            data.country=form.cleaned_data['country']
            data.city=form.cleaned_data['city']
            data.state=form.cleaned_data['state']
            data.order_total=total
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            #genetate order number
            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+str(data.id)
            data.order_number=order_number
            data.save()

            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
            DATA = {
                'amount' : data.order_total*100,
                'currency' : 'INR',
                'payment_capture' : 1,
            }
            payment = client.order.create(data=DATA)


            print('***')
            print(payment)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'payment' : payment,
            }
            return render(request,'payments.html',context)
    else:
        return redirect('checkout')
    



def order_complete(request):
    
    order_number = request.GET.get('order_id')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID': payment.payment_id,
            'payment': payment

        }
        return render(request, 'order_complete.html',context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('order_complete')

 

    
    
            




