from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect

from carts.models import Cart, CartItem
from carts.views import _cart_id
from order.models import Order, OrderProduct
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages,auth

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from store.models import Product

import requests

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    

    context = {
        'products': products,
    }
    return render(request,'home.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            phone_number  = form.cleaned_data['phone_number']
            email  = form.cleaned_data['email']
            password  = form.cleaned_data['password']
            username=email.split("@")[0]
            user= Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
            user.phone_number = phone_number
            user.save()

            #user activation
            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message = render_to_string('account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send(
                
            )
            #messages.success(request,'Thank you for register with us...verify your email address')
            messages.success(request,'Registration successful')
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request,'register.html',context)
        
        


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    # get the cart items from the user access 
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    # product_variation = [1, 2, 3, 4, 6]
                    # ex_var_list = [4, 6, 3, 5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
                   
            except:    
                pass

            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                
                params= dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                
            except:
                return redirect('home')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('login')

    return render(request,'login.html')

@login_required(login_url = 'login')
def logout(request):
   auth.logout(request)
   messages.success(request,'You are logged out.')
   return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congradulations! Your account is activated. ')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register') 


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # reset pasword email
            current_site = get_current_site(request)
            mail_subject = 'Reset your Password'
            message = render_to_string('reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your mail address')
            return redirect('login')

        else:
            messages.error(request,'Account does not exist')
            return redirect('forgotPassword')
    return render(request, 'forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid 
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('resetPassword')
    else:
        return render(request,'resetPassword.html')


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    UserProfile.objects.get_or_create(user=request.user)
    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'orders_count':orders_count,
        'userprofile' : userprofile,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders' : orders,
    }
    return render(request, 'my_orders.html',context)


@login_required(login_url="login")
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'userprofile' : userprofile,
    }
    return render(request, 'edit_profile.html', context)


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter correct password')
        else:
            messages.error(request, 'Passwords does not match')
            return redirect("change_password")
    return render(request, 'change_password.html')



def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)

    try:
        if order.status == 'Accepted':
            order_detail.is_shipped = True
        else:
            order_detail.is_shipped = False
    except:
        pass
    try:
        if order.status == 'Completed':
            order_detail.is_delivered = True
            order_detail.is_shipped = True
        else:
            order_detail.is_delivered = False
    except:
        pass

    
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context = {
        'order_detail' : order_detail,
        'order' : order,
        'subtotal' : subtotal,
        'is_shipped': order_detail.is_shipped,
        'is_delivered': order_detail.is_delivered,
        
    }
    return render(request, 'order_detail.html', context)



    