from rest_framework import serializers
from .models import Blog
from .models import User


class BlogSerializer(serializers.ModelSerializer):
    blog_title = serializers.CharField(source='title') # rename the api key
    class Meta:
        model = Blog
        fields = ['id', 'blog_title', 'description']

    def validate_title(self, value):
        """
        Validations single field
        """
        if len(value) < 10:
            raise serializers.ValidationError("Title must have at least 10 charectors")
        
        return value
    
    def to_representation(self, instance):
        """
        Adding extra fields that not in model
        """
        representation = super().to_representation(instance)
        representation['description_length'] = len(instance.description)
        return representation


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, data):
        """
        Validate all the fields
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("password and confirm password dosen't matched")
        
        return data
