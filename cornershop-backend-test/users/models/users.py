"""User model."""

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from utils.models import CommonModel


class User(CommonModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    email = models.EmailField(
        "email address",
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    is_manager = models.BooleanField(
        "manager",
        default=False,
        help_text=(
            "Help easily distinguish users and perform queries. "
            "managers are the main type of user."
        ),
    )

    def __str__(self):
        """Return username."""
        return self.username

    def get_full_name(self):
        """Return full name user."""
        return f"{self.first_name} {self.last_name}"
