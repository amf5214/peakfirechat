from flask import Flask, render_template, request, redirect, url_for, json, Response, jsonify, make_response, flash
from sqlalchemy.orm.exc import NoResultFound

from src.authentication import *
from src.image_handling import *
from src.models import AuthAccount, UserAccount, MessageGroupSubscription, Message, MessageGroup, db

def get_users_group_subs(user_id):
    subscriptions = db.session.execute(db.select(MessageGroupSubscription).filter_by(subscriber=user_id)).scalars()
    return [x for x in subscriptions]

