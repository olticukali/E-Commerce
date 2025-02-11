from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages

def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get Billing Info From Last Page
        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')

        # Gather Prder Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        # Create Shipping Address from session info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

        # Create an Order
        if request.user.is_authenticated:
            # logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name = full_name, email=email, shipping_address = shipping_address, amount_paid = amount_paid)
            create_order.save()
            messages.success(request, "Order Placed!")
            return redirect('home')
        else:
            # not logged in
            # Create Order
            create_order = Order(full_name = full_name, email=email, shipping_address = shipping_address, amount_paid = amount_paid)
            create_order.save()
            messages.success(request, "Order Placed!")
            return redirect('home')
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a sesion with Shippinf Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        # Check to see if user is loggen in
        if request.user.is_authenticated:
            # Get The Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, 'quantities': quantities, "totals": totals, 'shipping_info': request.POST, 'billing_form': billing_form})
        else:
            # Not logged in
            # Get The Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, 'quantities': quantities, "totals": totals, 'shipping_info': request.POST, 'billing_form': billing_form})
        
        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products": cart_products, 'quantities': quantities, "totals": totals, 'shipping_form': shipping_form})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def checkout(request):
     # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    if request.user.is_authenticated:
        # Checkout as logged in user
        # Shipping User
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance = shipping_user)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, 'quantities': quantities, "totals": totals, 'shipping_form': shipping_form})
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, 'quantities': quantities, "totals": totals, 'shipping_form': shipping_form})

def payment_success(reqeust):
    return render(reqeust, "payment/payment_success.html", {})