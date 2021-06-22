"""Menu Options model."""

# Django
from django.db import models

# Utilities
from utils.models import CommonModel

# Menu options Models
from .menu_options import Option


class Menu(CommonModel):
    """Menu model.
    This model is in charge of managing the daily menus
    """

    # name of menu
    name = models.CharField(max_length=150, blank=False, null=False)

    # Date for Menu
    date = models.DateField(
        auto_now_add=False,
        blank=False,
        null=False
    )
    # activate reminder
    reminder = models.BooleanField(
        'reminder',
        default=False,
        help_text='Activate reminder.'
    )

    options = models.ManyToManyField(
        Option, blank=True, related_name='menu_options', db_table='menus_menus_options')

    def __str__(self):
        """Return Menu name and date """
        return f"{self.name}-{self.date}"
