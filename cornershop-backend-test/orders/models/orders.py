"""Order model."""

from django.db import models

from utils.models import CommonModel


class Order(CommonModel):
    """Menu model.
    This model is in charge of managing the orders of the employees for their menu of the day
    """

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    menu = models.ForeignKey("menus.Menu", on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, blank=False, null=False)
    option = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        """Return Order User and date """
        return "{username} - {menu} - {option} at {date}".format(
            username=self.user.username,
            option=self.option,
            menu=self.menu,
            date=self.menu.date.strftime("%Y-%m-%d"),
        )
