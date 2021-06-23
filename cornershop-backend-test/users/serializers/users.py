"""Users serializers."""

# utisl python
import random
import string

# Django Hashers
from django.contrib.auth.hashers import make_password

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
            'created',
            'modified',
        )

    def create(self, data):
        """Handle user creation."""
        password = ''.join(random.choice(string.digits) for i in range(15))
        data['password'] = make_password(password)
        user = User.objects.create_user(**data)
        # send_confirmation_email.delay(user_pk=user.pk, password)
        return user
