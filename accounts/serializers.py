# serializers.py
from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile_picture', 'bio', 'role', 'profile_picture_url']
        read_only_fields = ['id']

    def get_profile_picture_url(self, obj):
        return obj.get_profile_picture_url()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Get the default token data
        data = super().validate(attrs)
        
        # Add custom user data
        user_data = CustomUserSerializer(self.user).data
        data['user'] = user_data
        
        return data
    
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # Call the base class's validate method
        
        # You can add custom data to the response here if needed
        # For example, add custom user data or additional fields
        
        return data