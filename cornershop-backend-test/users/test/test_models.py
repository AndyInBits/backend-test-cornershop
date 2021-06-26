from django.test import TestCase

from users.models import User


class UserModelTest(TestCase):
    """Test Model User"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User.objects.create(
            username="Admin",
            first_name="Bob",
            last_name="Bob",
            email="bob@tescase.com",
            phone_number="+1900000000",
        )

    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("username").verbose_name
        self.assertEqual(field_label, "username")

    def test_username_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("username").max_length
        self.assertEqual(max_length, 150)

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_first_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 30)

    def test_last_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_last_name_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 150)

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email address")

    def test_email_unique(self):
        user = User.objects.get(id=1)
        unique = user._meta.get_field("email").unique
        self.assertEqual(unique, True)

    def test_phone_number_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("phone_number").verbose_name
        self.assertEqual(field_label, "phone number")

    def test_phone_number_max_length(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field("phone_number").max_length
        self.assertEqual(max_length, 17)

    def test_is_manager_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("is_manager").verbose_name
        self.assertEqual(field_label, "manager")

    def test_is_manager_default(self):
        user = User.objects.get(id=1)
        default = user._meta.get_field("is_manager").default
        self.assertEqual(default, False)

    def test_str_object(self):
        user = User.objects.get(id=1)
        expected_object_name = user.username
        self.assertEqual(expected_object_name, str(user))

    def test_get_full_name(self):
        user = User.objects.get(id=1)
        expected_object_name = f"{user.first_name} {user.last_name}"
        self.assertEqual(expected_object_name, user.get_full_name())
