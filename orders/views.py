from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime

from .forms import CartAddForm, CouponForm
from .cart import Cart
from .models import Order, OrderItem, Coupon
from products.models import Product


# Create your views here.
class CartView(View):
    template_name = 'orders/cart.html'

    def get(self, request):
        cart = Cart(request)

        context = {'cart': cart}
        return render(request, self.template_name, context)


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cart.add(product, form.cleaned_data['quantity'])
        return redirect('orders:cart')

class CartRemoveView(View):
	def get(self, request, product_id):
		cart = Cart(request)
		product = get_object_or_404(Product, id=product_id)
		cart.remove(product)
		return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    template_name = 'orders/order.html'
    form_class = CouponForm

    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)

        context = {
            'order': order,
            'form': self.form_class
        }
        return render(request, self.template_name, context)


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
            )
        cart.clear()
        return redirect('orders:order_detail', order.id)


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        messages.success(request, 'Order paid successfully.', 'success')
        order.delete()
        return redirect('products:products')


class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponForm

    def post(self, request, order_id):
        now = datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(
                    code=code,
                    valid_form__lte=now,
                    valid_to__gte=now,
                    is_active=True
                )
            except Coupon.DoesNotExist:
                messages.error(request, 'coupon does not exist', 'danger')
                return redirect('orders:order_detail', order_id)

            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect('orders:order_detail', order_id)
            