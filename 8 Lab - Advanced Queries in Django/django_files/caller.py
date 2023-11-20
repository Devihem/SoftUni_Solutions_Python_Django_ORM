import os

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct
from django.db.models import Count, Sum, F, Q, Case, When
from decimal import Decimal


# Create and check models
def add_records_to_database():
    # Categories
    food_category = Category.objects.create(name='Food')
    drinks_category = (Category.objects.create(name='Drinks'))

    # Food
    product1 = Product.objects.create(name='Pizza', description='Delicious pizza with toppings', price=10.99,
                                      category=food_category, is_available=False)
    product2 = Product.objects.create(name='Burger', description='Classic burger with cheese and fries', price=7.99,
                                      category=food_category, is_available=False)
    product3 = Product.objects.create(name='Apples', description='A bag of juicy red apples', price=3.99,
                                      category=food_category, is_available=True)
    product4 = Product.objects.create(name='Bread', description='A freshly baked loaf of bread', price=2.49,
                                      category=food_category, is_available=True)
    product5 = Product.objects.create(name='Pasta and Sauce Bundle',
                                      description='Package containing pasta and a jar of pasta sauce', price=6.99,
                                      category=food_category, is_available=False)
    product6 = Product.objects.create(name='Tomatoes', description='A bundle of ripe, red tomatoes', price=2.99,
                                      category=food_category, is_available=True)
    product7 = Product.objects.create(name='Carton of Eggs', description='A carton containing a dozen fresh eggs',
                                      price=3.49, category=food_category, is_available=True)
    product8 = Product.objects.create(name='Cheddar Cheese', description='A block of aged cheddar cheese', price=7.99,
                                      category=food_category, is_available=False)
    product9 = Product.objects.create(name='Milk', description='A gallon of fresh cow milk', price=3.49,
                                      category=food_category, is_available=True)

    # Drinks
    product10 = Product.objects.create(name='Coca Cola', description='Refreshing cola drink', price=1.99,
                                       category=drinks_category, is_available=True)
    product11 = Product.objects.create(name='Orange Juice', description='Freshly squeezed orange juice', price=2.49,
                                       category=drinks_category, is_available=False)
    product12 = Product.objects.create(name='Bottled Water', description='A 12-pack of purified bottled water',
                                       price=4.99, category=drinks_category, is_available=True)
    product13 = Product.objects.create(name='Orange Soda', description='A 6-pack of carbonated orange soda', price=5.49,
                                       category=drinks_category, is_available=True)
    product14 = Product.objects.create(name='Bottled Green Tea', description='A bottled green tea', price=3.99,
                                       category=drinks_category, is_available=False)
    product15 = Product.objects.create(name='Beer', description='A bottled craft beer', price=5.49,
                                       category=drinks_category, is_available=True)

    # Customers
    customer1 = Customer.objects.create(username='john_doe')
    customer2 = Customer.objects.create(username='alex_alex')
    customer3 = Customer.objects.create(username='peter132')
    customer4 = Customer.objects.create(username='k.k.')
    customer5 = Customer.objects.create(username='peter_smith')

    # Orders
    order1 = Order.objects.create(customer=customer1)
    order_product1 = OrderProduct.objects.create(order=order1, product=product3, quantity=2)
    order_product2 = OrderProduct.objects.create(order=order1, product=product6, quantity=1)
    order_product3 = OrderProduct.objects.create(order=order1, product=product7, quantity=5)
    order_product4 = OrderProduct.objects.create(order=order1, product=product13, quantity=1)

    order2 = Order.objects.create(customer=customer3)
    order_product5 = OrderProduct.objects.create(order=order2, product=product3, quantity=2)
    order_product6 = OrderProduct.objects.create(order=order2, product=product9, quantity=1)

    order3 = Order.objects.create(customer=customer1)
    order_product5 = OrderProduct.objects.create(order=order3, product=product12, quantity=4)
    order_product6 = OrderProduct.objects.create(order=order3, product=product7, quantity=3)
    return "All data entered!"


# # Run and print your queries
# # print(add_records_to_database())
#
# # 2 Taking information from Orderproduct
# def product_quantity_ordered():
#     orders_query = OrderProduct.objects.values(name=F('product_id__name')).annotate(quantity=Sum('quantity')).order_by(
#         '-quantity')
#     new_list = []
#     for product in orders_query:
#         new_list.append(f"Quantity ordered of {product['name']}: {product['quantity']}")
#
#     return '\n'.join(new_list)
#
# # 2 Taking information from Products
# def product_quantity_ordered2():
#     orders_query = (Product.objects.
#                     filter(orderproduct__isnull=False).
#                     values('name').annotate(quantity=Sum('orderproduct__quantity')).
#                     order_by('-quantity'))
#
#     new_list = []
#     for product in orders_query:
#         new_list.append(f"Quantity ordered of {product['name']}: {product['quantity']}")
#
#     return '\n'.join(new_list)


# TASK 3
def ordered_products_per_customer():
    orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')
    final_log_print = []
    for order in orders:

        orders_query = order.orderproduct_set.all()

        final_log_print.append(f"Order ID: {order.id}, Customer: {order.customer.username}")

        for item in orders_query:
            final_log_print.append(f"- Product: {item.product.name}, Category: {item.product.category.name}")

    return '\n'.join(final_log_print)


# TASK4

def filter_products():
    query = Q(price__gt=3.00) & Q(is_available=True)

    filtered_query = Product.objects.filter(query).order_by('-price', 'name')

    items_list_print = [
        f"{item.name}: {item.price}lv."
        for item in filtered_query]

    return '\n'.join(items_list_print)


# print(filter_products())

# TASK 5


def give_discount():
    items_log_print = []

    items = Product.objects.filter(is_available=True).annotate(
        new_price=Case(
            When(price__gt=3.00, then=F('price') * Decimal(0.70)),
            default=F('price'))).order_by('-new_price', 'name')

    for q in items:
        items_log_print.append(f"{q.name}: {round(q.new_price, 2)}lv.")

    return '\n'.join(items_log_print)

# print(give_discount())
