from django.shortcuts import get_object_or_404, render, redirect
from products.forms import AddProductForm
from .models import *
from authenticate.models import Account
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from decimal import Decimal
from django.db.models import Q

def product(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category', None)
    if selected_category:
        products = Product.objects.filter(category__id=selected_category)
    else:
        products = Product.objects.all()
    
    account = None
    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass
    
    return render(request, 'products/product.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'accounts': account
    })

def addProduct(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.save()
            return redirect('products')
    else:
        form = AddProductForm()
    return render(request, 'products/addproduct.html', {'form': form, 'categories': categories})

def editProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    else:
        form = AddProductForm(instance=product)
    return render(request, 'products/addproduct.html', {'form': form, 'categories': categories})


def deleteProduct(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('products')


def product_search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', None)
    account = None

    if request.user.is_authenticated:
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            pass

    search_filter = Q(name__icontains=query)
    if category_id:
        search_filter &= Q(category__id=category_id)

    products = Product.objects.filter(search_filter)
    categories = Category.objects.all()

    return render(request, 'products/product.html', {
        'products': products,
        'accounts': account,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    })

