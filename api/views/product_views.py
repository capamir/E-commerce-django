from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from products.models import Product, Category
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

@api_view(['POST'])  
@permission_classes([IsAdminUser])
def create_product(request):
    data = request.data
    category = Category.objects.get(slug=data['category'])

    product = Product.objects.create(
        category=category,
        name=data['name'],
        slug=data['slug'],
        description=data['description'],
        price=data['price'],
        available=data['available']
    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])  
@permission_classes([IsAdminUser])
def update_product(request, product_id):
    data = request.data

    try:
        product = Product.objects.get(id=product_id)
        
        product.category = data['category']
        product.name = data['name']
        product.slug=data['slug'],
        product.description=data['description'],
        product.price=data['price'],
        product.available=data['available']

        product.save()

        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except:
        message = {'derail': 'Product not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)

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


@api_view(['POST'])  
@permission_classes([IsAdminUser])
def upload_product_image(request):
    data = request.data
    try:
        product_id = data['product_id']
        product = Product.objects.get(id=product_id)

        product.product_image = request.FILES.get('image')
        product.save()

        return Response('Image was uploaded successfully') 
    except:
        message = {'derail': 'Product not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
