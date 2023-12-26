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
    
    @app.route('/home/<int:group_id>')
    def chat_view(group_id):
        accounts = get_users_in_group(group_id)[0]
        accounts = [x[1] for x in accounts]
        user = get_account(request)
        if int(user.id) in accounts:
            chat = get_group_data(group_id)
            return render_template('chat_view.html', useraccount=user, chat=chat, group_id=group_id)
        else:
            return redirect('/')
        
    @app.route('/newmessage', methods=['POST'])
    def new_message():
        group_id = request.form["group-id"]
        accounts = get_users_in_group(group_id)[0]
        accounts = [x[1] for x in accounts]
        user = get_account(request)
        if int(user.id) in accounts:
            new_message = Message(sender=user.id, group=group_id, text=request.form["message-text"], is_visible=1)
            try:
                db.session.add(new_message)
                db.session.commit()
                return redirect(f'/home/{group_id}')
            except Exception as e:
                print(e)
                return redirect(f'/home/{group_id}')
        else:
            return redirect('/')

    # Routing for admin pages
    app.add_url_rule('/admin/uploadimage', methods=['GET'], view_func=AdminPageRendering.adminuploadimage)
    app.add_url_rule('/uploadimagedb', methods=["POST"], view_func=AdminPageRendering.uploadnewimage)
    app.add_url_rule('/permissions/requests/admin', view_func=AdminPageRendering.permissions_requests_admin)
    app.add_url_rule('/prequestdeny/<requestid>', view_func=AdminPageRendering.deny_request)
    app.add_url_rule('/prequestapprove/<requestid>', view_func=AdminPageRendering.approve_request)



    # Routing for profile pages
    app.add_url_rule('/signin/home', view_func=ProfilePageRendering.signin)
    app.add_url_rule('/signin/failed', view_func=ProfilePageRendering.failed_signin)
    app.add_url_rule('/profile', view_func=ProfilePageRendering.profile)
    app.add_url_rule('/attemptedsignin', methods=['POST'], view_func=ProfilePageRendering.signinattempt)
    app.add_url_rule('/signout', view_func=ProfilePageRendering.sign_out)
    app.add_url_rule('/newaccount', methods=['POST'], view_func=ProfilePageRendering.create_new_account)
    app.add_url_rule('/requestpermission/<permission>/<accountid>', view_func=ProfilePageRendering.create_permission_request)
    app.add_url_rule('/profileimageupdate', methods=['POST'], view_func=ProfilePageRendering.profileimageupdate)
    app.add_url_rule('/updateprofileattribute', methods=['POST'], view_func=ProfilePageRendering.updateprofileattribute)

    