from datetime import datetime

from django.test import TestCase

from menus.models import Menu, Option


class MenuOptionModelTest(TestCase):
    """Test Model Menu Options"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Option.objects.create(
            option="Arroz con pollo",
        )

    def test_option_label(self):
        option = Option.objects.get(id=1)
        field_label = option._meta.get_field("option").verbose_name
        self.assertEqual(field_label, "option")

    def test_comment_max_length(self):
        option = Option.objects.get(id=1)
        max_length = option._meta.get_field("option").max_length
        self.assertEqual(max_length, 500)

    def test_option_not_null(self):
        option = Option.objects.get(id=1)
        null = option._meta.get_field("option").null
        self.assertEqual(null, False)

    def test_option_not_blank(self):
        option = Option.objects.get(id=1)
        null = option._meta.get_field("option").blank
        self.assertEqual(null, False)


class MenuModelTest(TestCase):
    """Test Model Menu """

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods

        Menu.objects.create(
            name="menu of day",
            date=datetime.now().strftime("%Y-%m-%d"),
            reminder=True,
            available=True,
        )

    def test_menu_uuid_label(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field("menu_uuid").verbose_name
        self.assertEqual(field_label, "menu uuid")

    def test_menu_uuid_not_editable(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field("menu_uuid").editable
        self.assertEqual(field_label, False)

    def test_menu_uuid_unique(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field("menu_uuid").unique
        self.assertEqual(field_label, True)

    def test_name_label(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_name_not_null(self):
        menu = Menu.objects.get(id=1)
        null = menu._meta.get_field("name").null
        self.assertEqual(null, False)

    def test_name_not_blank(self):
        menu = Menu.objects.get(id=1)
        null = menu._meta.get_field("name").blank
        self.assertEqual(null, False)

    def test_name_max_length(self):
        menu = Menu.objects.get(id=1)
        max_length = menu._meta.get_field("name").max_length
        self.assertEqual(max_length, 150)

    def test_date_unique(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field("date").unique
        self.assertEqual(field_label, True)

    def test_date_not_blank(self):
        menu = Menu.objects.get(id=1)
        null = menu._meta.get_field("date").blank
        self.assertEqual(null, False)

    def test_date_not_null(self):
        menu = Menu.objects.get(id=1)
        null = menu._meta.get_field("date").null
        self.assertEqual(null, False)

    def test_date_auto_now(self):
        menu = Menu.objects.get(id=1)
        null = menu._meta.get_field("date").auto_now_add
        self.assertEqual(null, False)

    def test_reminder_label(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field("reminder").verbose_name
        self.assertEqual(field_label, "reminder")

    def test_reminder_default(self):
        menu = Menu.objects.get(id=1)
        default = menu._meta.get_field("reminder").default
        self.assertEqual(default, False)

    def test_reminder_help_text(self):
        menu = Menu.objects.get(id=1)
        help_text = menu._meta.get_field("reminder").help_text
        self.assertEqual(help_text, "Activate reminder.")

    def test_available_label(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field("available").verbose_name
        self.assertEqual(field_label, "available")

    def test_available_default(self):
        menu = Menu.objects.get(id=1)
        default = menu._meta.get_field("available").default
        self.assertEqual(default, True)

    def test_options_label(self):
        menu = Menu.objects.get(id=1)
        field_label = menu._meta.get_field("options").verbose_name
        self.assertEqual(field_label, "options")

    def test_options_blank(self):
        menu = Menu.objects.get(id=1)
        null = menu._meta.get_field("options").blank
        self.assertEqual(null, True)

    def test_options_db_table(self):
        menu = Menu.objects.get(id=1)
        db_table = menu._meta.get_field("options").db_table
        self.assertEqual(db_table, "menus_menus_options")
