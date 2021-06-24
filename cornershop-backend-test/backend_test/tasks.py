# celery logger and task
from menus.services.slack import send_message_slack
import time
from .celery import app
from celery.utils.log import get_task_logger
# date time lib
from datetime import datetime

# # Menu Model
from menus.models.menus import Menu

# Logger celery
logger = get_task_logger(__name__)

# service send menssage slack


@app.task(name="disabled_menu_today")
def disabled_menu_today():
    """ Periodic task that will be executed at 11:00 am to deactivate the menu of the day """
    now = datetime.now().strftime('%Y-%m-%d')
    Menu.objects.filter(date=now, available=True).update(available=False)


@app.task(name="send_menu_slack")
def send_menu_slack():
    """ send menu daily slack every days at 9:00 am """
    now = datetime.now().strftime('%Y-%m-%d')
    try:
        menu = Menu.objects.get(date=now, available=True)
        send_message_slack(menu.menu_uuid)
    except Menu.DoesNotExist:
        pass
