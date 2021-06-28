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


## Command to lift the project
### Running the development environment


```bash
$ make up
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
see demo here :
<video width="320" height="320" controls>
  <source src="https://github.com/Anfevazu/backend-test-cornershop/blob/master/Documentation/videos/admin.mp4" type="video/mp4">
</video>




## - Order manager:
- Users of this role can manage all the menus and see the orders of the employees, they can also activate or deactivate menus and the actions of sending the daily notification of the menus to the slack channel.

## - Employee :
- This role can only access to place orders and review your order history.
