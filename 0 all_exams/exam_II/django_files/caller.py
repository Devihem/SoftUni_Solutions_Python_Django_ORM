import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Create and run your queries within functions


import os
import django
from django.db.models import Count, Q, F, When, Case, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from _decimal import Decimal
from datetime import datetime, timedelta
from main_app.models import Product, Order, Profile


def get_profiles(search_string=None):
    result_print_log = []

    if isinstance(search_string, str):
        result_print_log = []
        profiles_selected = Profile.objects.filter(
            Q(full_name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_number__icontains=search_string)

        ).annotate(orders_count=Count('order')).order_by('full_name')

        for profile in profiles_selected:
            result_print_log.append(
                f"Profile: {profile.full_name}, email: {profile.email}, phone number: {profile.phone_number}, orders: {profile.orders_count}")

        return '\n'.join(result_print_log)
    return ""


def get_loyal_profiles():
    result_print_log = []
    profiles_selected = Profile.objects.get_regular_customers()

    if profiles_selected:
        for profile in profiles_selected:
            result_print_log.append(
                f"Profile: {profile.full_name}, orders: {profile.orders_count}"
            )

    return '\n'.join(result_print_log)


def get_last_sold_products():
    result_print_log = ''
    last_order = Order.objects.last()

    if last_order:
        product_list = [product.name for product in last_order.products.all().order_by('name')]
        result_print_log = f"Last sold products: {', '.join(product_list)}"

    return result_print_log


def get_top_products():
    result_print_log = []
    products = Product.objects.annotate(times_ordered=Count("order")).filter(times_ordered__gt=0).order_by(
        "-times_ordered", "name")[:5]

    if products:
        result_print_log = ["Top products:"]
        for product in products:
            result_print_log.append(
                f"{product.name}, sold {product.times_ordered} times"
            )

    return '\n'.join(result_print_log)


def apply_discounts():
    discounted_orders = Order.objects.annotate(
        ordered_times=Count('products')).filter(
        is_completed=False,
        ordered_times__gt=2).update(
        total_price=F('total_price') * 0.90)

    return f"Discount applied to {discounted_orders} orders."


def complete_order():
    oldest_order_nc = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if oldest_order_nc:

        for product in oldest_order_nc.products.all():
            # # Remove 1 unit.
            # oldest_order_nc.products.update(in_stock=(F('in_stock') - 1))
            #
            # # Remove them from Availability
            # oldest_order_nc.products.filter(in_stock__lt=1).update(is_available=False)

            product.in_stock -=1

            if product.in_stock == 0:
                product.is_available = False

            product.save()

        oldest_order_nc.is_completed = True
        oldest_order_nc.save()

        return "Order has been completed!"
    return ""
