from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    