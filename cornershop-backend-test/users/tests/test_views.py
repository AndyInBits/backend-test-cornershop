from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from users.models import User

factory = Client()


class AuthViewTest(TestCase):
    """Test Views Auth"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(
            username="Admin",
            first_name="admin",
            last_name="admin",
            email="admin@admintest.com",
            password="pbkdf2_sha256$180000$wBXCxFVhGmdV$F4Wh75P4ZM7uS7N1Y3Yhzzlq19JqUemroty98sJaxfQ=",
            phone_number="+1300000000",
            is_manager=True,
            is_staff=True,
            is_superuser=True,
        )

    def test_auth_credentials_invalid(self):
        """ validate get token using credentials invalid """

        response = factory.post(
            reverse("users_login"),
            data={"email": "admin1@yopmail.com", "password": "Admin123#"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_credentials_valid(self):
        """ validate get token using credentials valid """

        response = factory.post(
            reverse("users_login"),
            data={"email": "admin@admintest.com", "password": "Admin123#"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token_invalid(self):
        """ validate refresh token using headers invalid """
        response = factory.post(
            reverse("users_login"),
            data={"email": "admin@admintest.com", "password": "Admin123#"},
            content_type="application/json",
        )
        data = response.data
        headers = {"Authorization": f"Bearer {data['access']}"}
        response = factory.post(
            reverse("users_refresh_token"),
            data={"refresh": data["refresh"] + "invalid"},
            content_type="application/json",
            **headers,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_valid(self):
        """ validate refresh token using headers valid """
        response = factory.post(
            reverse("users_login"),
            data={"email": "admin@admintest.com", "password": "Admin123#"},
            content_type="application/json",
        )
        data = response.data
        headers = {"Authorization": f"Bearer {data['access']}"}
        response = factory.post(
            reverse("users_refresh_token"),
            data={"refresh": data["refresh"]},
            content_type="application/json",
            **headers,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_me_invalid(self):
        """ validate get me service using token invalid """
        response = factory.get(reverse("users_get_me"), content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_me_valid(self):
        """ validate get me service using token valid """
        response_auth = factory.post(
            reverse("users_login"),
            data={"email": "admin@admintest.com", "password": "Admin123#"},
            content_type="application/json",
        )
        data = response_auth.data
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + data["access"]
        response = factory.get(reverse("users_get_me"), content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserViewSetTest(TestCase):
    """ Test UserViewSet """

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(
            username="Admin",
            first_name="admin",
            last_name="admin",
            email="admin@admintest.com",
            password="pbkdf2_sha256$180000$wBXCxFVhGmdV$F4Wh75P4ZM7uS7N1Y3Yhzzlq19JqUemroty98sJaxfQ=",
            phone_number="+1300000000",
            is_manager=True,
            is_staff=True,
            is_superuser=True,
        )

    def setUp(self):
        """ Initial setup """
        response = factory.post(
            reverse("users_login"),
            data={"email": "admin@admintest.com", "password": "Admin123#"},
            content_type="application/json",
        )
        self.token = response.data["access"]
        self.url = "/api/v1/users/"
        self.user = User.objects.get(email="admin@admintest.com")

    def test_list_user(self):
        """ validate get List Users """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.get(
            self.url,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """ validate create Users """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.post(
            self.url,
            data={
                "username": "andresvz91",
                "first_name": "andres",
                "last_name": "vasquez",
                "email": "andresvz91@gmail.com",
                "phone_number": "+57 3000000031",
                "is_manager": True,
                "is_superuser": True,
                "is_staff": True,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_put_user(self):
        """ validate edit put Users """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.put(
            self.url + str(self.user.pk) + "/",
            data={
                "username": "andresvz91s",
                "first_name": "andress",
                "last_name": "vasquezz",
                "email": "admin@admintest.com",
                "phone_number": "+57 3000000032",
                "is_manager": True,
                "is_superuser": True,
                "is_staff": True,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_patch_user(self):
        """ validate edit patch Users """
        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.patch(
            self.url + str(self.user.pk) + "/",
            data={
                "username": "andresvz91",
                "first_name": "andres",
                "last_name": "vasquez",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        """ validate delete User """

        factory.defaults["HTTP_AUTHORIZATION"] = "Bearer " + self.token
        response = factory.delete(
            self.url + str(self.user.pk) + "/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
