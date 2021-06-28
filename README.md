# Cornershop's Backend Test

See technical requirements [Here !](https://github.com/Anfevazu/backend-test-cornershop/blob/master/Documentation/technical_requirements.md)

Development by [Andres Vasquez](https://github.com/anfevazu)

## Project description

Platform to manage the shipment of food from Cornershop employees

## Project technologies

- Python
- Django
- Docker
- Compose
- postgres
- celery
- redis
- nextJs
- Reactjs
- Django rest framework
- Slack SDK


## Branches of the project

- master

## System default users

- admin : admin1@yopmail.com - Admin123#
- order manager : menumanager@yopmail.com - Admin123#
- employee : employee@yopmail.com - Admin123#
-------


```bash
$ make up
```
## Run test
```bash
$ dev test
```
## Run test and details
```bash
$ dev apptest
```

- After this step load the base users of the system with the following command :
```bash
$ dev loaduser
```
- After having all the containers ready and the default data, you can proceed to execute the following command to start the python server :
```bash
$ dev up
```
- After this in another console raise celery and celery beat for the management of asynchronous tasks

```bash
$ dev celery
```
```bash
$ dev celerybeat
```

Luego de ejecutar estos comandos el projecto se levantara de la siguiente manera :

## Project urls

- Backend services : http://localhost:8000/
- Frontend : http://localhost:3000/
----------

# How does the system work ?

The system is based on 3 basic roles with different permissions that allow each role to perform different actions, these roles are: Admin, order manager and employees.

## - Admin:
- The users of this role can administer the system users, manage other admins, manage order managers or manage employees, basically this role is a super admin of the system which can be extended more functionalities but for the scope of the project it is only in charge of user management.
## [See demo here !](https://drive.google.com/file/d/155t2FEQcUPDID_q3qbmRpuIaAqPjHqtF/view?usp=sharing)


## - Order manager:
- Users of this role can manage all the menus and see the orders of the employees, they can also activate or deactivate menus and the actions of sending the daily notification of the menus to the slack channel.
## [See demo here !](https://drive.google.com/file/d/1Ru8tiYNk3ZZQIVhIIzBLRD-iwahOmS1c/view?usp=sharing)

## - Employee :
- This role can only access to place orders and review your order history.
## [See demo here !](https://drive.google.com/file/d/1d4AdkiJZHdhwnKAZ168r1nCaxUFpIxoS/view?usp=sharing)

____
### [See all videos !](https://github.com/Anfevazu/backend-test-cornershop/blob/master/Documentation/videos/)

___________

## Technical description of the project


- Data base diagram :
![DB](https://github.com/Anfevazu/backend-test-cornershop/blob/master/Documentation/images/bd.png?raw=true)

## App models :

- Common model - utils/models :
```python
class CommonModel(models.Model):
    """Delivery Manager base model.

    CommonModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        "created at",
        auto_now_add=True,
        help_text="Date time on which the object was created.",
    )
    modified = models.DateTimeField(
        "modified at",
        auto_now=True,
        help_text="Date time on which the object was last modified.",
    )

    class Meta:
        """Meta option."""

        abstract = True
        get_latest_by = "created"
        ordering = ["-created", "-modified"]
```


- User model - users/models :
```python
class User(CommonModel, AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    email = models.EmailField(
        "email address",
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )

    phone_regex = RegexValidator(
        regex=r"\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    is_manager = models.BooleanField(
        "manager",
        default=False,
        help_text=(
            "Help easily distinguish users and perform queries. "
            "managers are the main type of user."
        ),
    )

    def __str__(self):
        """Return username."""
        return self.username

    def get_full_name(self):
        """Return full name user."""
        return f"{self.first_name} {self.last_name}"

```
- Order model - orders/models :
```python
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

```

- Menu model - menus/models/menus :
```python
class Menu(CommonModel):
    """Menu model.
    This model is in charge of managing the daily menus
    """

    menu_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # name of menu
    name = models.CharField(max_length=150, blank=False, null=False)

    # Date for Menu
    date = models.DateField(auto_now_add=False, blank=False, null=False, unique=True)
    #  activate reminder
    reminder = models.BooleanField(
        "reminder", default=False, help_text="Activate reminder."
    )

    available = models.BooleanField("available", default=True)

    options = models.ManyToManyField(
        Option, blank=True, related_name="menu_options", db_table="menus_menus_options"
    )

    def __str__(self):
        """Return Menu name and date """
        return f"{self.name}-{self.date}"

```

- Menu Option model - menus/models/menus_options :
```python
class Option(CommonModel):
    """Option model.
    This model is in charge of managing the menu options of the day
    """

    option = models.TextField(max_length=500, blank=False, null=False)

    def __str__(self):
        """Return option's str representation."""
        return self.option

```
_______

## App Async Task celery :

- users/tasks :
    - send_welcome_email :
send the welcome email to a user with their credentials at the moment of being created by the super admin.

- menus/tasks :
    - disabled_menu_today : This task is executed every day at 11:00 am in Chile and deactivates the menu so that orders cannot be made from this menu and it is not available on the web.
    - send_menu_slack: This task is responsible for sending the menu every day at 9:00 am Chile time, this sends the menu to the following Slack channel: https://test-corners-shop.slack.com/archives/ C025WRTBD29

- orders/tasks :
    - confirm_order_email : This task sends a notification email to the employee after confirming an order.
____

# Endpoints Backend :
```Json
{
	"item": [
		{
			"name": "Users CRUD",
			"item": [
				{
					"name": "List Users",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NDg5ODc2LCJqdGkiOiJhN2ZhYjM0MWE3Mjg0NzZjODdhOWFmY2Y0MzcyN2ZlNyIsInVzZXJfaWQiOjF9.nrdemVJz_a2YMzZeaOHDf2kAnw0aFJF2SfQiEQJ8TmI",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/users/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"users",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Create Users",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NTY3MjY4LCJqdGkiOiJiZTAyMDc3ZTQ2YzA0NWQ3ODZjYTI0ZmNmNmNiMjA5NSIsInVzZXJfaWQiOjJ9.145WtaPbZwuz-BePpqHtI9QKB-Ra-qxEKjalVAz1mfM",
									"type": "string"
								}
							]
						},
						"method": "POST",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n        \"username\": \"andresvz91\",\n        \"first_name\": \"andres\",\n        \"last_name\": \"vasquez\",\n        \"email\": \"andresvz91@gmail.com\",\n        \"phone_number\": \"+57 3000000031\",\n        \"is_manager\": true,\n        \"is_superuser\": true,\n        \"is_staff\": true\n    }",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/users/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"users",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Update PUT User",
					"request": {
						"method": "PUT",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"username\": \"dsadsdsds\",\n    \"first_name\": \"Nosras\",\n    \"last_name\": \"pesdidos\",\n    \"email\": \"dsdsdsd@yosspmgail.scomm\",\n    \"phone_number\": \"+57 3000000031\",\n    \"is_manager\": false,\n    \"is_superuser\": false,\n    \"is_staff\": false\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/users/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"users",
								"7",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Get User",
					"request": {
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/users/8/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"users",
								"8",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Update PATH User",
					"request": {
						"method": "PATCH",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n  \n    \"first_name\": \"otra\",\n    \"last_name\": \"cosa\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/users/7",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"users",
								"7"
							]
						}
					},
					"response": []
				},
				{
					"name": "Delete Users",
					"request": {
						"method": "DELETE",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/users/5",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"users",
								"5"
							]
						}
					},
					"response": []
				}
			]
		},
		{
			"name": "Authentication",
			"item": [
				{
					"name": "Login Users",
					"request": {
						"method": "POST",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"email\": \"admin1@yopmail.com\",\n    \"password\": \"Admin123#\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/login",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"login"
							]
						}
					},
					"response": []
				},
				{
					"name": "Refresh Token",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NDg0MzkwLCJqdGkiOiI3YTNhYmQ3NGU5Mjg0ZmVhOTJjMmRhOWZhN2Y0ZTQ4OCIsInVzZXJfaWQiOjF9.S4P6C8mYKwnK4Cc6kIQWI2LKVdS79iFCpRO5xl1teF0",
									"type": "string"
								}
							]
						},
						"method": "POST",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"refresh\": \"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNDQ4NDM5MCwianRpIjoiYjNmY2NlNmEzNTU2NDI1YzgwMGQwMGNjYTk5YmRmMTIiLCJ1c2VyX2lkIjoxfQ.aCbegakNZIj1z2pTOiId-UScGLYeYVV9z5xEil_E4oY\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/token/refresh",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"token",
								"refresh"
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Me",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NDg2MjQxLCJqdGkiOiI0NzBhMzBkOGVmNjU0N2UwYTEzMzI2N2U5MThlOTg3NCIsInVzZXJfaWQiOjF9.H0tqyFQ1Q1alEaKp8abruPmUfYBODNYYEa5gJbSb8mI",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/get/me",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"get",
								"me"
							]
						}
					},
					"response": []
				}
			]
		},
		{
			"name": "Menu CRUD",
			"item": [
				{
					"name": "List Menus",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NjYxMjA5LCJqdGkiOiJkZWRhN2RkMzM5MjU0NjA1YjZjNzhlMjQxNThlOTY5YyIsInVzZXJfaWQiOjF9.4l3ltkoMHFcFs2plmPgvNnDXsPntwmlMuHU0QEFH2KM",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/menus/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menus",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Create Menu",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NjYxMjA5LCJqdGkiOiJkZWRhN2RkMzM5MjU0NjA1YjZjNzhlMjQxNThlOTY5YyIsInVzZXJfaWQiOjF9.4l3ltkoMHFcFs2plmPgvNnDXsPntwmlMuHU0QEFH2KM",
									"type": "string"
								}
							]
						},
						"method": "POST",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n        \"name\": \"Menu del Dia hoy\",\n        \"date\": \"2021-06-28\",\n        \"reminder\": true,\n        \"available\": false,\n        \"options\": [1,2,3,4]\n    }",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/menus/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menus",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Menu",
					"request": {
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/menus/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menus",
								"7",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Menu for UUID",
					"request": {
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/today/menu/b265820c-0e25-4977-adfd-c2cf38f22554",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"today",
								"menu",
								"b265820c-0e25-4977-adfd-c2cf38f22554"
							]
						}
					},
					"response": []
				},
				{
					"name": "Update PUT Menu",
					"request": {
						"method": "PATCH",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"name\": \"Menu del Dia hoy\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/menus/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menus",
								"7",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Update PATH Menu",
					"request": {
						"method": "PUT",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"pk\": 7,\n    \"name\": \"Menu del Dia dsdshoy\",\n    \"date\": \"2021-06-20\",\n    \"reminder\": true,\n    \"options\": [\n        5,\n        6\n    ]\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/menus/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menus",
								"7",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Delete Menu",
					"request": {
						"method": "DELETE",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/menus/6/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menus",
								"6",
								""
							]
						}
					},
					"response": []
				}
			]
		},
		{
			"name": "Orders CRUD",
			"item": [
				{
					"name": "List Orders",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NjYxMjA5LCJqdGkiOiJkZWRhN2RkMzM5MjU0NjA1YjZjNzhlMjQxNThlOTY5YyIsInVzZXJfaWQiOjF9.4l3ltkoMHFcFs2plmPgvNnDXsPntwmlMuHU0QEFH2KM",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/orders/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"orders",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Create Order",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NjYxMjA5LCJqdGkiOiJkZWRhN2RkMzM5MjU0NjA1YjZjNzhlMjQxNThlOTY5YyIsInVzZXJfaWQiOjF9.4l3ltkoMHFcFs2plmPgvNnDXsPntwmlMuHU0QEFH2KM",
									"type": "string"
								}
							]
						},
						"method": "POST",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"menu\": 1,\n    \"comment\": \"dsadasdsa\",\n    \"email\": \"andresvz91@gmail.com\",\n    \"password\": \"Admin123#\",\n    \"option\": \"Arroz con pollo\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/orders/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"orders",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Order",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NTU5NzcwLCJqdGkiOiJiNmNmMjdkMDI1YWU0MDhlODY3NTA1MzZlYzRlMDhjZSIsInVzZXJfaWQiOjN9._Z0WOC5UGH74V5vvXl1Mkaz73lfXrHa4GGtFkxu0n1U",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/orders/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"orders",
								"7",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Update PUT Order",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NTU5NzcwLCJqdGkiOiJiNmNmMjdkMDI1YWU0MDhlODY3NTA1MzZlYzRlMDhjZSIsInVzZXJfaWQiOjN9._Z0WOC5UGH74V5vvXl1Mkaz73lfXrHa4GGtFkxu0n1U",
									"type": "string"
								}
							]
						},
						"method": "PATCH",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n       \n       \"comment\": \"dsadasdsagfdgdfgfdg\"\n    }",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/orders/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"orders",
								"7",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Update PATH Order",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NTU5NzcwLCJqdGkiOiJiNmNmMjdkMDI1YWU0MDhlODY3NTA1MzZlYzRlMDhjZSIsInVzZXJfaWQiOjN9._Z0WOC5UGH74V5vvXl1Mkaz73lfXrHa4GGtFkxu0n1U",
									"type": "string"
								}
							]
						},
						"method": "PUT",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"menu\": 7,\n    \"comment\": \"dsadasdsa\",\n    \"user\": 8\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/orders/2/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"orders",
								"2",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Delete Order",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NTU5NzcwLCJqdGkiOiJiNmNmMjdkMDI1YWU0MDhlODY3NTA1MzZlYzRlMDhjZSIsInVzZXJfaWQiOjN9._Z0WOC5UGH74V5vvXl1Mkaz73lfXrHa4GGtFkxu0n1U",
									"type": "string"
								}
							]
						},
						"method": "DELETE",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/orders/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"orders",
								"7",
								""
							]
						}
					},
					"response": []
				}
			]
		},
		{
			"name": "Menu Options CRUD",
			"item": [
				{
					"name": "List Menu Options",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NjYxMjA5LCJqdGkiOiJkZWRhN2RkMzM5MjU0NjA1YjZjNzhlMjQxNThlOTY5YyIsInVzZXJfaWQiOjF9.4l3ltkoMHFcFs2plmPgvNnDXsPntwmlMuHU0QEFH2KM",
									"type": "string"
								}
							]
						},
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/menu/options/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menu",
								"options",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Create Menu Options",
					"request": {
						"auth": {
							"type": "bearer",
							"bearer": [
								{
									"key": "token",
									"value": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI0NjYxMjA5LCJqdGkiOiJkZWRhN2RkMzM5MjU0NjA1YjZjNzhlMjQxNThlOTY5YyIsInVzZXJfaWQiOjF9.4l3ltkoMHFcFs2plmPgvNnDXsPntwmlMuHU0QEFH2KM",
									"type": "string"
								}
							]
						},
						"method": "POST",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "  {\n       \n        \"option\": \"una cosa\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/menu/options/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menu",
								"options",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Get Menu Option",
					"request": {
						"method": "GET",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/menu/options/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menu",
								"options",
								"7",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Update PUT Menu Option",
					"request": {
						"method": "PATCH",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"option\": \"otra cosa\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/menu/options/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menu",
								"options",
								"7",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Update PATH Menu Option",
					"request": {
						"method": "PUT",
						"header": [],
						"body": {
							"mode": "raw",
							"raw": "{\n    \"option\": \"otra cosa\"\n}",
							"options": {
								"raw": {
									"language": "json"
								}
							}
						},
						"url": {
							"raw": "http://localhost:8000/api/v1/menu/options/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menu",
								"options",
								"7",
								""
							]
						}
					},
					"response": []
				},
				{
					"name": "Delete Menu Option",
					"request": {
						"method": "DELETE",
						"header": [],
						"url": {
							"raw": "http://localhost:8000/api/v1/menu/options/7/",
							"protocol": "http",
							"host": [
								"localhost"
							],
							"port": "8000",
							"path": [
								"api",
								"v1",
								"menu",
								"options",
								"7",
								""
							]
						}
					},
					"response": []
				}
			]
		}
	]
}

```
## Testing end points using  this : [Postman collection](https://github.com/Anfevazu/backend-test-cornershop/blob/master/Documentation/CornersShopTest.postman_collection.json)
