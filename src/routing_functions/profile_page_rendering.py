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

