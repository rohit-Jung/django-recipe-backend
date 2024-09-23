# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from django.contrib.auth import authenticate, login as auth_login
from rest_framework_simplejwt.tokens import AccessToken
from django.middleware.csrf import get_token
from django.contrib.auth import logout as django_logout, login
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import json

@api_view(['POST'])
def custom_token_refresh_view(request):
    try:
        # Call the parent class's post method to handle the token refresh
        view = TokenRefreshView.as_view(serializer_class=CustomTokenRefreshSerializer)
        response = view(request)
    except (InvalidToken, TokenError) as e:
        # If the token refresh fails, clear the cookies
        response = Response({'detail': 'Token refresh failed'}, status=status.HTTP_401_UNAUTHORIZED)
        response.set_cookie(
            'access_token',
            "",
            httponly=True,
            secure=True,  # Use this in production with HTTPS
            samesite='None',
        )
        response.set_cookie(
            'refresh_token',
            "",
            httponly=True,
            secure=True,  # Use this in production with HTTPS
            samesite='None',
        )
        
        # Set CSRF token in the response
        response.set_cookie(
            'csrftoken',
            "",
            httponly=False,  # CSRF token must be accessible by JavaScript
            secure=True,  # Use this in production with HTTPS
            samesite='None',
        )
    return response
    
@api_view(['POST'])
def register(request):
    if CustomUser.objects.filter(username=request.data.get('username')).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    if CustomUser.objects.filter(email=request.data.get("email")).exists():
        return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        print(user) 
        user.set_password(request.data.get('password'))  # Hash password
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"detail": "No active account found with the given credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = CustomTokenObtainPairSerializer(data={'username': username, 'password': password})
    if serializer.is_valid():
        tokens = serializer.validated_data
        access_token = tokens.get('access')
        refresh_token = tokens.get('refresh')
        
        response = Response({
            'data': serializer.validated_data,
            'csrf_token': get_token(request), 
        }, status=status.HTTP_200_OK)

        # Setting cookies
        response.set_cookie(
            'access_token',
            str(access_token),
            httponly=True,
            secure=request.is_secure(),  # Use HTTPS setting dynamically
            samesite='None',
        )
        response.set_cookie(
            'refresh_token',
            str(refresh_token),
            httponly=True,
            secure=request.is_secure(),  # Use HTTPS setting dynamically
            samesite='None',
        )
        
        # Set CSRF token
        csrf_token = get_token(request)
        response.set_cookie(
            'csrftoken',
            csrf_token,
            httponly=False,
            secure=request.is_secure(),
            samesite='None',
        )

        login(request, user)
        return response

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            RefreshToken(refresh_token).blacklist()

        django_logout(request)
        
        response = Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        
        # Clear cookies
        response.set_cookie('access_token', '', httponly=True, secure=True, samesite='None')
        response.set_cookie('refresh_token', '', httponly=True, secure=True, samesite='None')
        response.set_cookie('csrftoken', '', httponly=False, secure=True, samesite='None')
        
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    print("user", user)

    if not user:
        return Response({"detail": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    csrf_token = request.COOKIES.get('csrftoken')

    serializer = CustomUserSerializer(user)

    response_data = {
        'data': serializer.data,
        'access': access_token,
        'refresh': refresh_token,
        'csrf_token': csrf_token
    }

    return Response(response_data, status=status.HTTP_200_OK)

    """
    Log out and blacklist the refresh token.
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            RefreshToken(refresh_token).blacklist()

        django_logout(request);
        
        response = Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        
        response.set_cookie(
            'access_token',
            "",
            httponly=True,
            secure=True,  # Use this in production with HTTPS
            samesite='None',
        )
        response.set_cookie(
            'refresh_token',
            "",
            httponly=True,
            secure=True,  # Use this in production with HTTPS
            samesite='None',
        )
        
        # Set CSRF token in the response
        response.set_cookie(
            'csrftoken',
            "",
            httponly=False,  # CSRF token must be accessible by JavaScript
            secure=True,  # Use this in production with HTTPS
            samesite='None',
        )
        
        return response
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    data = request.data
    try:
        profile_picture = data.get('profile_picture')
        if profile_picture == "undefined" or not profile_picture:
            profile = user.profile_picture

        user_update_data = {
            'first_name': data.get('first_name', user.first_name),
            'last_name': data.get('last_name', user.last_name),
            'email': data.get('email', user.email),
            'username': data.get('username', user.username),
            'bio': data.get('bio', user.bio),
            'profile_picture': profile,  
            'role': data.get('role', user.role),
            
        }

        print("data prepared", user_update_data)

        serializer = CustomUserSerializer(user, data=user_update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    except json.JSONDecodeError as e:
        return Response({'error': f'Invalid JSON format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_list_create(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if user != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if user != request.user and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({"message": "User deleted"},  status=status.HTTP_204_NO_CONTENT)
