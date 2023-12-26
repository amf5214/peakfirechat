from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, render_template, request, redirect, url_for, json, Response, jsonify, make_response, flash
import sys
import os
from datetime import datetime, timedelta, date, timezone
from werkzeug.utils import secure_filename
import uuid
import logging
from base64 import b64encode
import base64
from io import BytesIO #Converts data from Database into bytes
from sqlalchemy import create_engine
import pymysql

from src.models import FileContent, db
def render_picture(data):
    """Converts byte data for image into a viewable format that is safe for browsers

    Accepts stream data of raw image and converts it into a byte stream that is able to be rendered via a browser
    
    Keyword Arguements:
    data -- stream with raw image data

    Return: base64 string with browser safe version of the image

    """

    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

