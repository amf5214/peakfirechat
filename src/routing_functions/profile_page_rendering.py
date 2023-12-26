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


    def signinattempt():
        """View function that handles a sign in attempt

        Takes a post request in the form of an html form submission. If the signin works then user redirected to home path
        otherwise user will be redirected to failed sign in path.

        Return: Redirect object that moves the user to the correct page based off accuracy of the submitted form 
        
        """

        try:
            given_pass = request.form["logpass"]

            auth_account = db.session.execute(db.select(AuthAccount).filter_by(email_account=request.form["logemail"])).scalar_one()

            if(validate_password(given_pass, auth_account.hash_password)):
                token_data = encode_auth_token(request.form["logemail"])
                auth_account.auth_token = token_data[0]
                auth_account.token_key = token_data[1]
                db.session.commit()
                response = make_response(redirect("/"))
                response.set_cookie("token", auth_account.auth_token)
                return response
            else:
                return redirect("/signin/failed")
        except NoResultFound: 
            return redirect("/signin/failed")
    
    def sign_out():
        """View function that handles a sign out attempt

        Function signs out current user by setting auth token cookie to None

        Return: Response that redirects to home path 

        """

        response = make_response(redirect("/"))
        response.set_cookie("token", "None")
        return response

    def create_new_account():
        """View function that handles the creation of a new account

        Function creates a new user account using post request in the form of an html form submission

        Return: Redirect to either the home path or to the sign in page

        """

        if request.form["logname"]=="No Account":
            return render_template('signinup.html', signupmessage="Name entry is invalid", useraccount=get_account(request))

        password = create_password(request.form["logpass"])
        token_data = encode_auth_token(str(request.form["logusername"]))
        auth_account = AuthAccount(email_account=request.form["logemail"],hash_password=password, auth_token=token_data[0], token_key=token_data[1])

        db.session.add(auth_account)

        db.session.commit()

        authaccountrec = db.session.execute(db.select(AuthAccount).filter_by(email_account=request.form["logemail"])).scalar_one()
        try:   
            birthdatedata=birthdate=request.form["logbirthdate"].split("-")
            birthdate = date(int(birthdatedata[0]), int(birthdatedata[1]), int(birthdatedata[2]))
            account = UserAccount(username=request.form["logusername"],full_name=request.form["logname"],birthdate=birthdate,auth_account_id=authaccountrec.id)
        except ValueError:
                    account = UserAccount(username=request.form["logusername"],full_name=request.form["logname"],auth_account_id=authaccountrec.id)
        db.session.add(account)
        db.session.commit()
        return redirect('/signin/home')

    def create_permission_request(permission, accountid):
        """View function that handles the creation of a permissions request

        Function that handles the creation of permission request.

        Keyword Arguement:
        permission -- string representing requested permission
        accountid -- integer representing user account id

        Return: Redirect to the profile page

        """

        account = UserAccount.query.get_or_404(accountid)
        request = PermissionsRequest(account_id=accountid, permission_type=permission, username=account.username, grant_date=date.today())
        db.session.add(request)
        db.session.commit()
        return redirect('/profile')

    def profileimageupdate():
        """View function that handles a request to update a user's profile image

        Function that handles a request to update a user's profile picture. Accepts a 
        post request in the form of an html form submission. Utilizes uploadimage function 
        from image_handling module.

        Return: Redirect to the profile page

        """

        image_id = uploadimage(request)
        picture_account = UserAccount.query.get_or_404(request.form["user_id"])

        picture_account.account_image_link = str(image_id)
        db.session.commit()
        return redirect("/profile")
    
