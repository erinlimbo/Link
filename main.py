import webapp2
import logging
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users
from datetime import date

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    dates_free = ndb.DateProperty(repeated=True)
    # friends = ndb.KeyProperty(repeated=True, kind=User) --> this is a many to many relationship

class Login(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/login.html')
        self.response.write(template.render(template_vars))
    def post(self):
        template_vars = {
            'username' : self.request.get('username'),
            'password': self.request.get('password'),
        }
        template = jinja_env.get_template('templates/login.html')
        self.response.write(template.render(template_vars))

class Home(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/home.html')
        self.response.write(template.render(template_vars))

class Profile(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        # first_name = users.name.familyName()
        template_vars = {
            'current_user': current_user,
            # 'first_name' : first_name
        }

        template = jinja_env.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))

class Friends(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/friends.html')
        self.response.write(template.render(template_vars))

class Schedule(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/schedule.html')
        self.response.write(template.render(template_vars))

    def post(self):
        template_vars = {
            "date": date(int(self.request.get("year")),
            int(self.request.get("month")),
            int(self.request.get("day")))
        }
        template = jinja_env.get_template('templates/linkup.html')
        self.response.write(template.render(template_vars))

class Linkup(webapp2.RequestHandler):
    def get(self):
        template_vars = {

        }
        template = jinja_env.get_template('templates/linkup.html')
        self.response.write(template.render(template_vars))

class populateDatabase(webapp2.RequestHandler):
    def get(self):
        Alexa = User(
            name = 'Alexa',
            email = 'alexa@gmail.com',
            dates_free = [date(2019, 11, 30), date(2019, 12, 12)]
        )

        self.redirect("/home")

app=webapp2.WSGIApplication([
    ('/', Login),
    ('/home', Home),
    ('/profile', Profile),
    ('/friends', Friends),
    ('/schedule', Schedule),
    ('/linkup', Linkup),
    ('/login', Login),
    ('/populateDatabase', populateDatabase),
], debug=True)
