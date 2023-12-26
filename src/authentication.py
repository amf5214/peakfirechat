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

