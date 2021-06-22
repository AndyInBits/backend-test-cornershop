"""Profile model."""

# Django
from django.db import models

# Utilities
from utils.models import CommonModel


class Profile(CommonModel):
    """Profile model.

    A profile holds a user's public data like biography, picture,
    and statistics.
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = models.TextField(blank=True, null=True)
    biography = models.TextField(max_length=500, blank=True)

    position = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
