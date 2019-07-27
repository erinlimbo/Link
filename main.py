import webapp2
import logging
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    dates_free = ndb.StringProperty(repeated=True)
    friends = ndb.KeyProperty(repeated=True, kind=User)

class MainPage(webapp2.RequestHandler):
    def get(self):

        template_vars = {

        }

        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render(template_vars))

app=webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
