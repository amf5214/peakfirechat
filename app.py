from flask import Flask
from sqlalchemy.exc import OperationalError
import os
import configparser
import secrets

app = Flask(__name__)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)