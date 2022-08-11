from django.contrib import messages,auth
from django.shortcuts import redirect, render
from shop.models import Account

from category.forms import CategoryForm
from category.models import Category
from order.models import Order, OrderProduct, Payment
from store.forms import ProductForm, VariationForm
from store.models import  Carousel, Product, Variation
from shop.models import Awesome
from shop.forms import CarouselForm
from django.template.defaultfilters import slugify
from django.db.models import Sum
from django.contrib.auth.decorators import login_required 
from django.db.models.functions import TruncMinute
import datetime
from django.db.models import Q




# Create your views here.

def adminlogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        admin = auth.authenticate(email=email, password=password)
        auth.login(request, admin)
        messages.success(request, 'login successful')
        return redirect('adminpanel')
    else:
        return render(request, 'adminpanel/admin_accounts/admin_login.html')


@login_required(login_url="login")
def user_accounts_table(request,id):
    if request.user.is_superadmin:
        active_users = Account.objects.all().filter(is_admin=False,is_active=True)
        banned_users = Account.objects.all().filter(is_admin = False, is_active =False)
        context  = {
            'active_users' : active_users,
            'banned_users' : banned_users,
        }
        if id==1:
            return render(request,'adminpanel/admin_accounts/active_users.html',context)
        else:
            return render(request,'adminpanel/admin_accounts/banned_users.html',context)
    else:
        return redirect ('home')


@login_required(login_url="login")
def ban_user(request,id):
    if request.user.is_superadmin:
        user           = Account.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect('user_accounts_table',id=1)
    else:
        return redirect ('home')


@login_required(login_url="login")
def unban_user(request,id):
    if request.user.is_superadmin:
        user           = Account.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect('user_accounts_table',id=2)
    else:
        return redirect ('home')
    


@login_required(login_url="login")
def category_table(request,id):
    if request.user.is_superadmin:
       
        category = Category.objects.all()
        
        context = {
            
            'category' : category,
           
        }
        
        return render(request,'adminpanel/category_table/category.html',context)
        
    else:
        return redirect ('home')



# category start

@login_required(login_url="login")
def add_category(request):
    if request.user.is_superadmin:
        form = CategoryForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST,request.FILES)
            if form.is_valid():
                category = form.save()
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                category.slug = slug
                category.save()
                messages.success(request,'New category added successfully')
                return redirect('category_table',id=2)
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/category_table/add_category.html',context)
    else:
        return redirect('home')

@login_required(login_url="login")
def edit_category(request,id):
    if request.user.is_superadmin:
        category = Category.objects.get(id=id)
        if request.method == 'POST':
            form = CategoryForm(request.POST,request.FILE, instance=category)
            if form.is_valid():
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                category = form.save()
                category.slug = slug
                category.save()
                messages.success(request,'category editted successfully')
                return redirect('category_table',id=2)
        else:
            form = CategoryForm(instance=category)
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/category_table/add_category.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def delete_category(request,id):
    if request.user.is_superadmin:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect ('category_table',id=2)
    else:
        return redirect ('home')

# category end

# 


           
@login_required(login_url="login")
def order_table(request,id):
    if request.user.is_superadmin:
        orders = Order.objects.filter(is_ordered=True,status='New')
        accepted_orders = Order.objects.filter(is_ordered=True,status='Accepted')
        completed_orders = Order.objects.filter(is_ordered=True,status="Completed")
        cancelled_orders = Order.objects.filter(is_ordered=True,status="Cancelled")
        order_products = OrderProduct.objects.all()
        payments = Payment.objects.all()
        context = {
            'orders' : orders,
            'order_products' : order_products,
            'payments' : payments,
            'accepted_orders' : accepted_orders,
            'completed_orders' : completed_orders,
            'cancelled_orders' : cancelled_orders,
        }

        if id==1:
            return render (request,'adminpanel/order_table/orders.html',context)
        elif id==2:
            return render(request,'adminpanel/order_table/order_products.html',context)   
        elif id==3:
            return render(request,'adminpanel/order_table/accepted_orders.html',context)
        elif id==4:
            return render(request,'adminpanel/order_table/completed_orders.html',context)
        elif id==5:
            return render(request,'adminpanel/order_table/cancelled_orders.html',context)
        else:
            return render(request,'adminpanel/order_table/payments.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_accepted(request,order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(id=order_id)
        order.status = 'Accepted'
        order.save()
        return redirect('order_table',id=1)
    else:
        return redirect ('home')


@login_required(login_url="login")
def order_completed(request,order_id):
    if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Completed'
        order.save()
        return redirect('order_table',id=2)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_cancelled(request,order_id):
    if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        return redirect('order_table',id=1 )
    else:
        return render(request,'adminpanel/order_table/order_cancelled.html')




@login_required(login_url="login")
def store_table(request,id):
    if request.user.is_superadmin:
        products = Product.objects.all()
        variations =Variation.objects.all()

        context = {
            'products' : products,
            'variations' : variations,
        }
        if id==1:
            return render(request,'adminpanel/store_table/products.html',context)
        else:
            return render(request,'adminpanel/store_table/variations.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def add_product(request):
    if request.user.is_superadmin:
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product_name = form.cleaned_data['product_name']
                slug = slugify(product_name)
                product.slug = slug
                product.save()
                                
                return redirect('store_table',id=1)
        else:
            form = ProductForm()
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/store_table/add_product.html',context)
    else:
        return redirect('home')

@login_required(login_url="login")
def edit_product(request,id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        if request.method =='POST':
            form = ProductForm(request.POST,request.FILES,instance=product)
            if form.is_valid():
                product_name = form.cleaned_data['product_name']
                slug = slugify(product_name)
                product = form.save()
                product.slug = slug
                product.save()

                
                return redirect('store_table',id=1)
        else:
            form = ProductForm(instance=product)
        context = {
            'form' : form,

        }
        return render (request,'adminpanel/store_table/add_product.html',context)
    else:
        return redirect ('home')


@login_required(login_url="login")
def delete_product(request,id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect('store_table',id=1)
    else:
        return redirect ('home')




@login_required(login_url="login")     
def add_variations(request):
    if request.user.is_superadmin:
        form = VariationForm()
        if request.method == 'POST':
            form = VariationForm(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                return redirect('store_table',id=2)
        else:
            form = VariationForm()
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/store_table/add_variations.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_variations(request,id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        if request.method =='POST':
            form = VariationForm(request.POST,instance=variation)
            if form.is_valid():
                form.save()
                return redirect('store_table',id=2)
        else:
            form = VariationForm(instance=variation)
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/store_table/add_variations.html',context)
    else:
        return redirect ('home')


@login_required(login_url="login")
def delete_variatons(request,id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        variation.delete()
        return redirect('store_table',id=2)
    else:
        return redirect ('home')




@login_required(login_url="login")
def home_table(request,id):
    if request.user.is_superadmin:
        carousels = Carousel.objects.all()
       
        awesomes = Awesome.objects.all()

        context = {
            'carousels' : carousels,
            
            'awesomes' : awesomes,
        }
        if id==1:
            return render(request,'adminpanel/home_table/carousel.html',context)
        elif id==2:
            return render(request,'adminpanel/home_table/awesomes.html',context)
        else:
            return render(request,'adminpanel/home_table/best_sellers.html',context)
    else: 
        return redirect ('home')


@login_required(login_url="login")
def add_carousels(request):
    if request.user.is_superadmin:
        form = CarouselForm()
        if request.method == 'POST':
            form = CarouselForm(request.POST,request.FILES)
            print(form)
            if form.is_valid():
                form.save()
                return redirect('home_table',id=1)
        else:
            form = CarouselForm()
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/home_table/add_carousel.html',context)
    else:
        return redirect('home')


@login_required(login_url="login")
def edit_carousel(request,id):
    if request.user.is_superadmin:
        carousel = Carousel.objects.get(id=id)
        if request.method =='POST':
            form = CarouselForm(request.POST,instance=carousel)
            if form.is_valid():
                form.save()
                return redirect('home_table',id=1)
        else:
            form = CarouselForm(instance=carousel)
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/home_table/add_carousel.html',context)
    else:
        return redirect ('home')


@login_required(login_url="login")   
def carousel_not_available(request,id):
    if request.user.is_superadmin:
        carousel           = Carousel.objects.get(id=id)
        carousel.is_available = False
        carousel.save()
        return redirect('home_table',id=1)
    else:
        return redirect ('home')


@login_required(login_url="login")
def caraousel_available(request,id):
    if request.user.is_superadmin:
        carousel           = Carousel.objects.get(id=id)
        carousel.is_available = True
        carousel.save()
        return redirect('home_table',id=1)
    else:
        return redirect ('home')


@login_required(login_url="login")
def delete_carousel(request,id):
    if request.user.is_superadmin:
        carousel = Carousel.objects.get(id=id)
        carousel.delete()
        return redirect('home_table',id=1)
    else:
        return redirect ('home')






@login_required(login_url="login")
def adminpanel(request):
    if request.user.is_superadmin:
        total_revenue = round( Order.objects.filter(is_ordered = True).aggregate(sum = Sum('order_total'))['sum'])


        total_cost= round((total_revenue * .80))
        total_profit = round(total_revenue - total_cost)  
        chart_year = datetime.date.today().year
        chart_month = datetime.date.today().month

        #getting daily revenue
        daily_revenue = Order.objects.filter(                     
            created_at__year=chart_year,created_at__month=chart_month
        ).order_by('created_at').annotate(day=TruncMinute('created_at')).values('day').annotate(sum=Sum('order_total')).values('day','sum')

        day=[]
        revenue=[]
        for i in daily_revenue:
            day.append(i['day'].minute)
            revenue.append(int(i['sum']))

        product_count = OrderProduct.objects.all().count()

        context = {
            'total_revenue' : total_revenue,
            'total_cost' : total_cost,
            'total_profit' : total_profit,
            'day' : day,
            'revenue' : revenue,
            'product_count' : product_count,
        }
        return render (request,'adminpanel/adminpanel.html',context)
    else:
        return redirect('adminlogin')


@login_required(login_url='adminpanel')
def admin_search(request):
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
           products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keywords) | Q(product_name__icontains=keywords))
            
        context = {
           
            'products':products,

        }
        
        return render(request,'adminpanel/store_table/products.html',context)
    return redirect('adminpanel')


def variationsearch(request):
    variations=[]
    if 'keywordss' in request.GET:
        keywordss=request.GET['keywordss']
    
        if keywordss:
            variations=Variation.objects.order_by('-created_date').filter(Q(variation_category__icontains=keywordss)|Q(variation_value__icontains=keywordss))
        context={
            'variations':variations,
        }
    return render(request,'adminpanel/store_table/variations.html',context)
def productsearch(request):
    products=[]
    if 'keywordss' in request.GET:
        keywordss=request.GET['keywordss']
    
        if keywordss:
            products=Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keywordss))
        context={
            'products':products,
        }
    return render(request,'adminpanel/store_table/products.html',context)
def adminuserdetails(request):
    user=[]
    if 'keywordss' in request.GET:
        
        keyword=request.GET['keywordss']
        if keyword:
            user=Account.objects.filter(Q(first_name__icontains=keyword)|Q(last_name__icontains=keyword)|Q(email__icontains=keyword)|Q(phone_number__icontains=keyword)|Q(username__icontains=keyword))
            print(user)
            context={
                'active_users':user,
                
            }
    return render(request,'adminpanel/admin_accounts/active_users.html',context)

def ordersearch(request):
    
    orders=[]
    if 'keywords' in request.GET:
        
        keyword=request.GET['keywords']
        if keyword:
            orders=OrderProduct.objects.order_by('-created_at').filter(Q(product__product_name__icontains=keyword)|Q(user__email__icontains=keyword))
            context={
                
                'order_products':orders,
            }
    return render(request,'adminpanel/order_table/order_products.html',context)