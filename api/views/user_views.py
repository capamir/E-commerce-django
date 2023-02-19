from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password

from api.serializers import UserSerializerWithToken, UserSerializer
from accounts.models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def register_User(request):
    data = request.data

    if request.user.is_authenticated:
        message = {'detail': 'you are logged in'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:        
            user = User.objects.create(
                email=data['email'],
                phone_number=data['phone_number'],
                full_name=data['full_name'],
                password=make_password(data['password'])
            )
            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'user with this emial or phone number is already registered'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)

    data = request.data
    user.email = data['email']
    user.phone_number = data['phone_number']
    user.full_name = data['full_name']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, many=False)

    except:
        message = {'detail': 'user not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        data = request.data
        
        user.email = data['email']
        user.phone_number = data['phone_number']
        user.full_name = data['full_name']
        user.is_admin = data['is_admin']
        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
        
    except:
        message = {'detail': 'user not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    user_for_deletion = User.objects.filter(id=user_id)
    if user_for_deletion.exists():
        user_for_deletion.delete()
        return Response('user deleted successfully')
    else:
        message = {'detail': 'user not found'}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
