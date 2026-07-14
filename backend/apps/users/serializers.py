"""
Serializers for user authentication, registration, and profile management.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, OwnerProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Handles user registration with password validation."""

    password = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'role', 'phone', 'gender',
            'city', 'college'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        # Create OwnerProfile if registering as owner
        if user.role == User.Role.OWNER:
            OwnerProfile.objects.create(user=user)

        return user


class UserLoginSerializer(serializers.Serializer):
    """Handles user login with email or username."""

    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not email and not username:
            raise serializers.ValidationError("Email or username is required.")

        # Try to find user by email first, then username
        user = None
        if email:
            try:
                user_obj = User.objects.get(email=email.lower())
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        elif username:
            user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        if user.is_suspended:
            raise serializers.ValidationError("Your account has been suspended. Contact support.")

        data['user'] = user
        return data


class GoogleAuthSerializer(serializers.Serializer):
    """Handles Google OAuth authentication."""

    token = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=User.Role.choices, default=User.Role.STUDENT)


class UserProfileSerializer(serializers.ModelSerializer):
    """Full user profile serializer with owner profile details."""

    owner_profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'gender', 'profile_picture', 'city',
            'college', 'is_verified', 'date_joined', 'last_active',
            'owner_profile'
        ]
        read_only_fields = ['id', 'email', 'role', 'is_verified', 'date_joined', 'last_active']

    def get_owner_profile(self, obj):
        if obj.role == User.Role.OWNER and hasattr(obj, 'owner_profile'):
            return OwnerProfileSerializer(obj.owner_profile).data
        return None


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Handles profile updates."""

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'gender',
            'profile_picture', 'city', 'college'
        ]


class OwnerProfileSerializer(serializers.ModelSerializer):
    """Serializer for owner business profile."""

    class Meta:
        model = OwnerProfile
        fields = [
            'business_name', 'business_address', 'id_proof',
            'is_verified_owner', 'total_properties', 'total_earnings'
        ]
        read_only_fields = ['is_verified_owner', 'total_properties', 'total_earnings']


class ChangePasswordSerializer(serializers.Serializer):
    """Handles password change."""

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect current password.")
        return value


class AdminUserListSerializer(serializers.ModelSerializer):
    """Serializer for admin user management listing."""

    properties_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'is_verified', 'is_suspended', 'is_active',
            'date_joined', 'last_active', 'properties_count'
        ]

    def get_properties_count(self, obj):
        if obj.role == User.Role.OWNER:
            return obj.properties.count()
        return 0
