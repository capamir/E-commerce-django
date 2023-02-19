from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from products.models import Product
from api.serializers import ProductSerializer

@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@api_view(['GET'])
def get_product_details(request, product_id):
    product = Product.objects.get(id=product_id)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])  
@permission_classes([IsAdminUser])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        product.delete()

        return Response('product deleted successfully')
    except:
        message = {'derail': 'Product not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
