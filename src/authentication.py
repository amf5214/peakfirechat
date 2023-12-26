from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError
from flask import Flask, render_template, request, redirect, url_for, json, Response, jsonify, make_response, flash
import sys
import os
from datetime import datetime, timedelta, date, timezone
import uuid
from base64 import b64encode
import base64
from io import BytesIO #Converts data from Database into bytes
from sqlalchemy import create_engine
import pymysql
import secrets

from src.models import AuthAccount, UserAccount, AccountPermission, FileContent, PermissionsRequest, db

def create_password(password_string):
    """Encrypts a password string

    Keyword Arguements:
    password_string = string value representing the password that needs to be encrypted

    Return: string
    """

    return sha256_crypt.encrypt(password_string)

def validate_password(given_pass, real_pass):
    """Valides user password by verifying that the crypt string equates to the provided unencrypted password
    
    Keyword Arguements:
    given_pass = unencrypted password string
    real_pass = crypt string that is being compared to 

    Return: boolean
    """

    return sha256_crypt.verify(given_pass, real_pass)

def get_auth_account(token):
    """Pulls an authentication account from the datatables

    Takes in a string representing the encoded jwt and decodes it using the stored secret key to access the expiration date and compare it. 
    For the token to still be valid, the delta of the expiration date and now should be negative, otherwise None will be returned

    Keyword Arguements:
    token -- string representing encoded jwt token

    Return: AuthAccount object
    """

    auth_account = db.session.execute(db.select(AuthAccount).filter_by(auth_token=token)).scalar_one()
    if auth_account:
        try:
            jwt.decode(token, key=auth_account.token_key, algorithms=["HS256"])
            return auth_account
        except jwt.ExpiredSignatureError:
            return None
    else:
        return None


