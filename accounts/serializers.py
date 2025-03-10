from rest_framework import serializers
from .models import UserAccount
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
UserAccount = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=UserAccount.objects.all())]
    )
    zip_code = serializers.CharField(
        max_length=20,
        required=False,
        validators=[RegexValidator(regex=r'^\d{5}(?:-\d{4})?$', message="Invalid zip code")]
    )
    phone_number = serializers.CharField(max_length=20, required=False)

    class Meta:
        model = UserAccount
        fields = ('username', 'email', 'password', 'password2', 'address', 'city', 'zip_code', 'phone_number', 'first_name', 'last_name')
        extra_kwargs = {
            'address': {'required': False},
            'city': {'required': False},
            'phone_number':{'required': False},
            'zip_code':{'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        try:
            user = UserAccount.objects.create_user(**validated_data)
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        return user
    


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(queryset=UserAccount.objects.all(), message="This email address is already in use.")],
        error_messages={
            'invalid': 'Enter a valid email address.',
        }
    )
    zip_code = serializers.CharField(
        max_length=20,
        required=False,
        validators=[RegexValidator(regex=r'^\d{5}(?:-\d{4})?$', message="Invalid zip code")],
        error_messages={
            'max_length': 'Zip code must be at most 20 characters long.',
        }
    )
    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        error_messages={
            'max_length': 'Phone number must be at most 20 characters long.',
        }
    )

    class Meta:
        model = UserAccount
        fields = ('first_name', 'last_name', 'email', 'address', 'city', 'zip_code', 'phone_number')
        read_only_fields = ('username',)
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'address': {'required': False},
            'city': {'required': False},
        }

    def update(self, instance, validated_data):
        changed = False
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                setattr(instance, attr, value)
                changed = True

        if changed:
            instance.save()
        return instance
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('id', 'username', 'email', 'address', 'city', 'zip_code')