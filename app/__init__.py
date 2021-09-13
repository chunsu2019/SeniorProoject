from flask import Flask
import os

app = Flask(__name__)

app.secret_key = 'abcdefghijklmn'

from app import views
from app import admin_views