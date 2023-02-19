from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from orders.models import Order, OrderItem, ShippingAddress, Coupon
from products.models import Product
from api.serializers import OrderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data
    order_items = data['orderItems']

    if order_items and len(order_items) == 0:
        message = {'detail': 'No order items'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:

        # (1) get coupon and Create order
        coupon = Coupon.objects.filter(code=data['coupon_code'])
        if coupon.exists():
            order = Order.objects.create(
                user=user,
                discount=coupon.discount
            )

        order = Order.objects.create(user=user)
        # (2) create shipping address
        shipping_address = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode']   
        )
        # (3) create order items and set order to order items relationship
        for item in order_items:
            product = Product.objects.filter(id=item['product'])
            if product.exists():
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity'],
                )
            else:
                message = {'detail': 'product not found'}
                return Response(message, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, order_id):
    user = request.user

    try:
        order = Order.objects.get(id=order_id)
        if request.user.is_admin or user == order.user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            message = {'detail': 'Not authorized to view this order'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'detail': 'order not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def update_order_to_paid(request, order_id):
    user = request.user

    try:
        order = Order.objects.get(id=order_id)
        if request.user.is_admin or user == order.user:
            order.paid = True
            order.save()
            return Response('order was paid')
        else:
            message = {'detail': 'Not authorized to view this order'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    except:
        message = {'detail': 'order not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)

