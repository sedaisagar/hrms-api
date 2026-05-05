from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields =[
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'phone_number',
            'date_of_birth',
            'photo',
            'role',
        ]
        extra_kwargs = {
            'role': {'read_only': True},    
        }
        

    def create(self, validated_data):
        role = self.context.get("role")
        validated_data.update(
            password=make_password(validated_data.get('password')),
            role = role,
        )
        return super().create(validated_data)
    