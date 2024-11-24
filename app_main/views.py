from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail

from app_main.models import Category, Product, Cart


class HomeView(ListView):
    model = Product
    template_name = 'app_main/home.html'
    paginate_by = 6
    context_object_name = 'products'
    extra_context = {
        'is_search': True
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset


class CategoriesView(ListView):
    model = Category
    template_name = 'app_main/categories.html'
    paginator_class = Paginator
    context_object_name = 'categories'
    paginate_by = 5
    extra_context = {
        'is_search': True
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset


class CategoryList(ListView):
    model = Product
    template_name = 'app_main/product-list.html'
    context_object_name = 'products'

    def get_queryset(self):

        category_id = self.kwargs.get('category_id')

        if category_id:
            return Product.objects.filter(category_id=category_id)
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.kwargs.get('category_id')
        if category_id:
            context['category'] = get_object_or_404(Category, id=category_id)

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_main/product-detail.html'
    context_object_name = 'products'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object
        return context


def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.info(request, 'you shoul')
        return redirect('login')

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        product=product, user=request.user,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Savat sahifasiga yo'naltirish
    return redirect('cart_view')


def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, product_id=product_id, user=request.user)

    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart_view')


def change_product_cart(request, product_id, action):
    cart_item = get_object_or_404(Cart, product__id=product_id, user=request.user)

    if action == 'increment':
        cart_item.quantity += 1

    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        elif cart_item.quantity == 1:
            cart_item.delete()
            return redirect('cart_view')

    cart_item.save()

    return redirect('cart_view')


def checkout(request):
    cart = request.session.get('cart', {})
    # if not cart:
    #     messages.error(request, "Your cart is empty.")
    #     return redirect('home')

    email = request.user.email
    if request.user.is_authenticated :
        product_details = []
        total_amount = 0

        for product_id, details in cart.items():
            product_name = details.get('name')
            quantity = details.get('quantity', 0)
            price = details.get('new_price', 0)
            total_price = price * quantity
            product_details.append(f"{product_name} - Quantity: {quantity}, Total: ${total_price}")
            total_amount += total_price

        shipping_cost = 10
        total_amount_with_shipping = total_amount + shipping_cost

        message = "\n".join(product_details)
        message += f"\n\nSubtotal: ${total_amount}\nShipping: ${shipping_cost}\nTotal Amount: ${total_amount_with_shipping}"

        send_mail(
            subject="Order Confirmation",
            message=message,
            from_email="odiloffr@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        request.session['cart'] = {}
        messages.success(request, "Your order has been placed successfully!")

        return redirect('home')
    else:
        return redirect('home')


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)

        total_price = sum(item.product.new_price * item.quantity for item in cart_items)

        return render(request, 'app_main/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            '10_day': date.today() + timedelta(days=10),
            'today': date.today(),
            'total_all': total_price + 10
        })
    else:
        messages.info(request, 'you should be logged in')
        return redirect('login')
