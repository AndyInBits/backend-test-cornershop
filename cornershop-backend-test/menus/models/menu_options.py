"""Menu Options model."""

# Django
from django.db import models

# Utilities
from utils.models import CommonModel


class Option(CommonModel):
    """Option model.
    This model is in charge of managing the menu options of the day
    """
    option = models.TextField(max_length=500, blank=False, null=False)

    def __str__(self):
        """Return option's str representation."""
        return self.option
