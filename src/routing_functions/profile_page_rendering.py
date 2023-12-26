from flask import Flask, render_template, request, redirect, url_for, json, Response, jsonify, make_response, flash
from sqlalchemy.orm.exc import NoResultFound

from src.authentication import *
from src.image_handling import *
from src.models import AuthAccount, UserAccount, db

Permission_values = ["Admin", "Edit_Pages", "Add_Pages"]

class Permission():
        def __init__(self, has, name):
            self.has=has
            self.name=name

class ProfilePageRendering():
    def signin():
        """View function that renders the signin/signup page

        Renders the page used to sign in and sign up for an account

        Return: Rendered view from signinup.html template with js and css code 

        """

        return render_template('signinup.html', useraccount=get_account(request))

    def failed_signin():
        """View function that renders the signin/signup page with error message due to a failed sign in

        Renders the page used to sign in and sign up for an account but adds the error message variable due to a failed sign in attempt

        Return: Rendered view from signinup.html template with js and css code 

        """

        return render_template('signinup.html', message="Username/Password Invalid. Please try again.", useraccount=get_account(request))

    def profile():
        """View function that renders the profile page

        Renders the page used to view user profile. Checks to ensure that there is a user signed in and 
        redirects to sign in page if no user is signed in

        Return: Rendered view from profile.html template with js and css code 

        """

        account = get_account(request)
        if account.full_name != "No Account":
            permissions = db.session.execute(db.select(AccountPermission).filter_by(account_id=account.id)).scalars()
            permissions_gen = []
            remaining_permissions = [z for z in Permission_values]
            for x in permissions:
                perm_type = x.permission_type
                permissions_gen.append(Permission(has=True, name=perm_type))
                remaining_permissions.remove(perm_type)
            for y in remaining_permissions:
                permissions_gen.append(Permission(has=False, name=y))
            return render_template("profile.html", useraccount=account, permissions=permissions_gen)
        else:
            return redirect('/signin/home')

# @app.route('/profile/introduction')
# def introduction():
#     return render_template("introduction.html", useraccount=get_account(request))


