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

    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('jumping.html', useraccount=get_account(request)), 404

    @app.route('/404')
    def error_404():
        return render_template('jumping.html', useraccount=get_account(request)), 404

    @app.route('/')
    def go_home():
        user = get_account(request)
        chats = get_chats_for_user(user.id)
        return render_template('index.html', useraccount=user, chats=chats)
    