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

