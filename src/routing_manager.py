from flask import render_template, request, redirect

from src.routing_functions.profile_page_rendering import ProfilePageRendering
from src.routing_functions.admin_page_rendering import AdminPageRendering

from src.authentication import get_account
from src.models import FileContent, Message, db
from src.image_handling import create_image
from src.messaging_functions import get_chats_for_user, get_group_data, get_users_in_group


def configure_routing(app):
    """Adds url rules to the main app object to route traffic to the correct view function

    Takes in a flask app object and adds url rules to it to route traffic to specific view functions based off the provided path

    Keyword Arguements:
    app -- flask app object

    Return: None
    """