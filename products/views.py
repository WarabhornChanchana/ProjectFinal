from django.shortcuts import get_object_or_404, render, redirect
from products.forms import AddproductForm
from .models import * 
from authenticate.models import Account
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from decimal import Decimal

def product(request):
    account = None
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass
    product = Product.objects.all()
    return render(request,'products/product.html',{'products':product,'accounts':account})



def addProduct(request):
    category = Category.objects.all()
    if request.method == 'POST':
        form = AddproductForm(request.POST, request.FILES)
        cat = Category.objects.get(name=request.POST.get('cat'))
        if form.is_valid():
            shipping_cost = request.POST.get('shipping_cost') 
            try:
                shipping_cost = Decimal(shipping_cost)  
            except:
                shipping_cost = None
            product_instance = form.save(commit=False)
            product_instance.category = cat
            product_instance.shipping_cost = shipping_cost
            product_instance.save()
            return redirect('products')
    else:
        form = AddproductForm()
    return render(request, 'products/addproduct.html', {'productform': form, 'categorys': category })


def editProduct(request, pk):
    product = Product.objects.get(id=pk) 
    if request.method == 'POST':
        form = AddproductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = AddproductForm(instance=product)
    return render(request, 'products/addproduct.html',{'productform':form})

def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('products')

def product_list(request):
    account = None
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass
    product = Product.objects.all()
    return render(request,'products/product.html',{'products':product,'accounts':account})


def product_search(request):
    query = request.GET.get('q', '')
    account = None
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass
    products = Product.objects.filter(name__icontains=query) 
    return render(request, 'products/product.html', {'products': products, 'accounts':account})
