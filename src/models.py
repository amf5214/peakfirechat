from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date, timezone

db = SQLAlchemy()

class UserAccount(db.Model):
    """Model representing the UserAccount table

    Holds data on every row of the UserAccount table
    
    Parent Classes:
    db.Model -- Model class from the database which provides access to the database schema 

    """
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    full_name = db.Column(db.String(100))
    auth_account_id = db.Column(db.Integer)
    birthdate = db.Column(db.Date)
    account_image_link = db.Column(db.String(100))
    bio = db.Column(db.Text)
    experience = db.Column(db.Text)

    def __repr__(self):
        return f"<UserAccount {self.id}>"
    
    def set_auth(self, auth_account):
        self.auth = auth_account
