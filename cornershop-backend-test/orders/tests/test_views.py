from datetime import datetime

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from menus.models import Menu
from orders.models import Order
from users.models import User

factory = Client()


class OrderViewSetTest(TestCase):

    """Test UserViewSet"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create(
            username="employee1",
            first_name="Bob",
            last_name="Bob",
            email="employee1@admin.com",
            phone_number="+1900000000",
            password="pbkdf2_sha256$180000$wBXCxFVhGmdV$F4Wh75P4ZM7uS7N1Y3Yhzzlq19JqUemroty98sJaxfQ=",
        )
        menu = Menu.objects.create(
            name="menu Test",
            date=datetime.now().strftime("%Y-%m-%d"),
            reminder=True,
            available=True,
        )
        Order.objects.create(
            menu=menu, comment="gluten frees", option="no suggar", user=user
        )

    def setUp(self):
        """ Initial setup """
        response = factory.post(
            reverse("users_login"),
            data={"email": "employee1@admin.com", "password": "Admin123#"},
            content_type="application/json",
        )
        self.token = response.data["access"]
        self.url = "/api/v1/orders/"
        self.order = Order.objects.get(comment="gluten frees")
        self.menu = Menu.objects.get(name="menu Test")

    def test_list_orders(self):
        """ validate get List Orders """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.get(
            self.url,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        """ validate create Orders """

        response = factory.post(
            self.url,
            data={
                "menu": self.menu.pk,
                "comment": "Con mucha salsa",
                "email": "employee1@admin.com",
                "password": "Admin123#",
                "option": "Arroz con pollo",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_put_orders(self):
        """ validate edit put orders """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.put(
            self.url + str(self.order.pk) + "/",
            data={
                "menu": self.menu.pk,
                "comment": "mejor sin salsa",
                "option": "Arroz con pollo",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_patch_order(self):
        """ validate edit patch Orders """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.patch(
            self.url + str(self.order.pk) + "/",
            data={"comment": "mejor sin salsa y con mucho arroz"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        """ validate delete Order """

        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.delete(
            self.url + str(self.order.pk) + "/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
