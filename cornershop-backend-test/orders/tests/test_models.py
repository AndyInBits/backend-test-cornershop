from datetime import datetime

from django.test import TestCase

from menus.models import Menu
from orders.models import Order
from users.models import User


class OrderModelTest(TestCase):

    """Test Model Order"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(
            username="Admin",
            first_name="Bob",
            last_name="Bob",
            email="admin@admin",
            phone_number="+1900000000",
        )
        menu = Menu.objects.create(
            name="menu of day",
            date=datetime.now().strftime("%Y-%m-%d"),
            reminder=True,
            available=True,
        )

        Order.objects.create(
            menu=menu, comment="gluten free", option="no suggar", user=user
        )

    def test_user_not_null(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field("user").null
        self.assertEqual(null, False)

    def test_menu_not_null(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field("menu").null
        self.assertEqual(null, False)

    def test_comment_label(self):
        order = Order.objects.get(id=1)
        field_label = order._meta.get_field("comment").verbose_name
        self.assertEqual(field_label, "comment")

    def test_comment_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field("comment").max_length
        self.assertEqual(max_length, 500)

    def test_comment_not_null(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field("comment").null
        self.assertEqual(null, False)

    def test_comment_not_blank(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field("comment").blank
        self.assertEqual(null, False)

    def test_option_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field("option").max_length
        self.assertEqual(max_length, 500)

    def test_option_null(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field("option").null
        self.assertEqual(null, True)

    def test_option_blank(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field("option").blank
        self.assertEqual(null, True)

    def test_str_object(self):
        order = Order.objects.get(id=1)
        expected_object_name = "{username} - {menu} - {option} at {date}".format(
            username=order.user.username,
            option=order.option,
            menu=order.menu,
            date=order.menu.date.strftime("%Y-%m-%d"),
        )
        self.assertEqual(expected_object_name, str(order))
