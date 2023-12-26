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

class AccountPermission(db.Model):
    """Model representing the AccountPermission table

    Holds data on every row of the AccountPermission table
    
    Parent Classes:
    db.Model -- Model class from the database which provides access to the database schema 

    """

    id = db.Column(db.Integer, primary_key=True)
    permission_type = db.Column(db.String(50))
    account_id = db.Column(db.Integer)
    grant_date = db.Column(db.Date)

    def __repr__(self):
        return f"<AccountPermission {self.id}>"
    
class PermissionsRequest(db.Model):
    """Model representing the PermissionsRequest table

    Holds data on every row of the PermissionsRequest table
    
    Parent Classes:
    db.Model -- Model class from the database which provides access to the database schema 

    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    permission_type = db.Column(db.String(50))
    account_id = db.Column(db.Integer)
    grant_date = db.Column(db.Date)
    is_visible = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"<AccountPermission Request {self.id}>"
    
class AuthAccount(db.Model):
    """Model representing the AuthAccount table

    Holds data on every row of the AuthAccount table
    
    Parent Classes:
    db.Model -- Model class from the database which provides access to the database schema 

    """

    id = db.Column(db.Integer, primary_key=True)
    email_account = db.Column(db.String(100), unique=True)
    hash_password = db.Column(db.String(1000))
    auth_token = db.Column(db.String(1000))
    token_key = db.Column(db.Text(4294967295))

    def __repr__(self):
        return f"<AuthAccount {self.id}>"

