import webapp2
import jinja2
import os
import time

from google.appengine.ext import ndb
from google.appengine.api import users

env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)
