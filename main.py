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

class User(ndb.Model):
    neighborhood = ndb.KeyProperty()
    firstname = ndb.StringProperty()
    lastname = ndb.StringProperty()
    email = ndb.StringProperty()
    admin_bool = ndb.BooleanProperty()

class Neighborhood(ndb.Model):
    admin = ndb.KeyProperty()
    code = ndb.StringProperty()
    zip_code = ndb.IntegerProperty()

class Post(ndb.Model):
    poster = ndb.KeyProperty() #the neighbor who posted
    content = ndb.StringProperty()
    category = ndb.StringProperty()
    neighborhood = ndb.KeyProperty()
    created_time = ndb.DateTimeProperty(auto_now_add=True)

class welcome(webapp2.RequestHandler):
    def get(self):

        login_url = users.create_login_url("/")

        template = env.get_template("templates/welcome.html")
        templateVars = { #this is a dictionary
            "login_url" : login_url,
        }

        self.response.write(template.render(templateVars))

class home(webapp2.RequestHandler):
    def get(self):

        user_query = User.query()
        user_list = user_query.fetch()

        current_user = users.get_current_user()
        current_neighbor = None
        current_neighborhood = None

        if current_user:
            current_email = current_user.email()
            current_neighbor = user_query.filter(User.email == current_email).get()
        else:
            self.redirect("/welcome")

        if current_neighbor:
            current_neighborhood = current_neighbor.neighborhood.get()
        else:
            self.redirect("/createaccount")


        post_query = Post.query()
        post_query = post_query.order(-Post.created_time)
        post_query = post_query.filter(Post.neighborhood == current_neighborhood)
        posts = post_query.fetch()

        logout_url = users.create_logout_url("/welcome")

        templateVars = { #this is a dictionary
            "current_user" : current_user,
            "posts" : posts,
            "user_list" : user_list,
            "logout_url" : logout_url,
            "current_neighbor" : current_neighbor,
            "current_neighborhood" : current_neighborhood,
        }
        template = env.get_template("templates/home.html")

        self.response.write(template.render(templateVars))

class createaccount(webapp2.RequestHandler):
    def get(self):

        template = env.get_template("templates/createaccount.html")
        templateVars = { #this is a dictionary
        }

        self.response.write(template.render(templateVars))

class chooseneighborhood(webapp2.RequestHandler):
    def get(self):

        template = env.get_template("templates/chooseneighborhood.html")
        templateVars = { #this is a dictionary
        }

        self.response.write(template.render(templateVars))

class createneighborhood(webapp2.RequestHandler):
    def get(self):

        template = env.get_template("templates/createneighborhood.html")
        templateVars = { #this is a dictionary
        }

        self.response.write(template.render(templateVars))

class profile(webapp2.RequestHandler):
    def get(self):

        template = env.get_template("templates/profile.html")
        templateVars = { #this is a dictionary
        }

        self.response.write(template.render(templateVars))


app = webapp2.WSGIApplication([
    ("/", home),
    ("/welcome", welcome),
    ("/createaccount", createaccount),
    ("/chooseneighborhood", chooseneighborhood),
    ("/createneighborhood", createneighborhood),
    ("/profile", profile),
    ("/adminconsole", adminconsle),
], debug=True)
