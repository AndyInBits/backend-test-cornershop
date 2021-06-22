"""Users serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class."""
        model = User
        fields = (
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_manager',
            'is_superuser',
            'is_staff',
        )

    def create(self, data):
        """Handle user creation."""
        data['password'] = User.objects.make_random_password()
        user = User.objects.create_user(**data)
        # send_confirmation_email.delay(user_pk=user.pk)
        return user
