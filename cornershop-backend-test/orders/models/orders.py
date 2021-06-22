"""Order model."""

# Django
from django.db import models

# Utilities
from utils.models import CommonModel


class Order(CommonModel):
    """Menu model.
    This model is in charge of managing the orders of the employees for their menu of the day
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    menu = models.ForeignKey('menus.Menu', on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, blank=False, null=False)

    def __str__(self):
        """Return Order User and date """
        return '{username} - {menu} at {date}'.format(
            user=self.user.username,
            menu=self.menu,
            date=self.menu.date.strftime('%Y-%m-%d'),
        )
