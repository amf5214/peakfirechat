from flask import Flask, render_template, request, redirect, url_for, json, Response, jsonify, make_response, flash
from sqlalchemy.orm.exc import NoResultFound

from src.authentication import *
from src.image_handling import *
from src.models import AuthAccount, UserAccount, MessageGroupSubscription, Message, MessageGroup, db

def get_users_group_subs(user_id):
    subscriptions = db.session.execute(db.select(MessageGroupSubscription).filter_by(subscriber=user_id)).scalars()
    return [x for x in subscriptions]

def get_messages_by_group(group_id):
    messages = db.session.execute(db.select(Message).filter_by(group=group_id)).scalars()
    messages_sorted = sorted(messages, key=lambda x: x.datetime_sent)
    messages_sent = [x for x in messages_sorted]
    for message in messages_sent:
        senders = db.session.execute(db.select(UserAccount).filter_by(id=message.sender)).scalars()
        if senders:
            senders = [x for x in senders]
            if senders[0].full_name != None:  
                message.sender_name = senders[0].full_name
            else:
                message.sender_name = senders[0].username
        else:
            message.sender_name = message.sender
    return messages_sent

