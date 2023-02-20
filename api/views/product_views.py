from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from products.models import Product, Category, Review
from api.serializers import ProductSerializer

@api_view(['GET'])
def get_products(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    # page = request.query_params.get('page')
    # paginator = Paginator(products, 5)

    # try:
    #     products = paginator.page(page)
    # except PageNotAnInteger:
    #     products = paginator.page(1)
    # except EmptyPage:
    #     products = paginator.page(paginator.num_pages)

    # if page == None:
    #     page = 1

    # page = int(page)

    products = Product.objects.filter(name__icontains=query)
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)
    # return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_review(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    data = request.data

    # (1) Review already exists
    already_exists = Product.review_set.filter(user=user).exists()
    if already_exists:
        message = {'detail': 'product already reviewed'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    # (2) No rating or 0
    elif data['rating'] == 0:
        message = {'detail': 'please select a rating'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
    # (3) Create Review
    else:
        review = Review.objects.create(
            product=product,
            user=user,
            name=user.full_name,
            rating=data['rating'],
            comment=data['comment']
        )
        return Response('review added successfully')
