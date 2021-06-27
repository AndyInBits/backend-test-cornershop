from datetime import datetime

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from menus.models import Menu, Option
from users.models import User

factory = Client()


class OptionViewSetTest(TestCase):
    """Test OptionViewSet"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            password="pbkdf2_sha256$180000$wBXCxFVhGmdV$F4Wh75P4ZM7uS7N1Y3Yhzzlq19JqUemroty98sJaxfQ=",
            phone_number="+1300000000",
            is_manager=True,
            is_staff=True,
            is_superuser=True,
        )

        Option.objects.create(
            option="Arroz con pollos",
        )

    def setUp(self):
        """ Initial setup """

        response = factory.post(
            reverse("users_login"),
            data={"email": "test@test.com", "password": "Admin123#"},
            content_type="application/json",
        )
        self.token = response.data["access"]
        self.url = "/api/v1/menu/options/"
        self.option = Option.objects.get(option="Arroz con pollos")

    def test_list_menu_options(self):
        """ validate get List menu options """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.get(
            self.url,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_menu_option(self):
        """ validate create menu option """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.post(
            self.url,
            data={"option": "una cosa"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_put_options(self):
        """ validate edit put Options """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.put(
            self.url + str(self.option.pk) + "/",
            data={"option": "Arroz con pollito"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_patch_options(self):
        """ validate edit patch Options """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.patch(
            self.url + str(self.option.pk) + "/",
            data={"option": "Arroz con pollito y salsa"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_option(self):
        """ validate delete option """

        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.delete(
            self.url + str(self.option.pk) + "/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MenuViewSetTest(TestCase):
    """Test MenuViewSet"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(
            username="test",
            first_name="test",
            last_name="test",
            email="test@test.com",
            password="pbkdf2_sha256$180000$wBXCxFVhGmdV$F4Wh75P4ZM7uS7N1Y3Yhzzlq19JqUemroty98sJaxfQ=",
            phone_number="+1300000000",
            is_manager=True,
            is_staff=True,
            is_superuser=True,
        )

        Option.objects.create(
            option="Frijol con arroz",
        )
        Option.objects.create(
            option="Carne",
        )

        Menu.objects.create(
            name="menu of day test",
            date=datetime.now().strftime("%Y-%m-%d"),
            reminder=True,
            available=True,
        )

    def setUp(self):
        """ Initial setup """

        response = factory.post(
            reverse("users_login"),
            data={"email": "test@test.com", "password": "Admin123#"},
            content_type="application/json",
        )
        self.token = response.data["access"]
        self.url = "/api/v1/menus/"
        self.menu = Menu.objects.get(name="menu of day test")
        self.option1 = Option.objects.get(option="Carne")
        self.option2 = Option.objects.get(option="Frijol con arroz")

    def test_list_menu(self):
        """ validate get List menu """

        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.get(
            self.url,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_menu(self):
        """ validate create menu """

        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.post(
            self.url,
            data={
                "name": "Menu del Dia hoy con sabor",
                "date": "2021-06-28",
                "reminder": True,
                "available": False,
                "options": [self.option1.pk, self.option1.pk],
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_put_menu(self):
        """ validate edit put Menu """

        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.put(
            self.url + str(self.menu.pk) + "/",
            data={
                "name": "Menu del Dia hoy con sabor",
                "date": "2021-06-29",
                "reminder": True,
                "available": True,
                "options": [self.option1.pk, self.option1.pk],
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_patch_menu(self):
        """ validate edit patch Menu """

        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.patch(
            self.url + str(self.menu.pk) + "/",
            data={
                "date": "2021-06-30",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_menu(self):
        """ validate delete menu """

        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.delete(
            self.url + str(self.menu.pk) + "/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
