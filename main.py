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
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    dates_free = ndb.StringProperty(repeated=True)
    friends = ndb.KeyProperty(repeated=True, kind='User')

class Login(webapp2.RequestHandler):
    def get(self):
        login_url = users.create_login_url('/')
        template_vars = {
            "login_url": login_url
         }
        template = jinja_env.get_template('templates/login.html')
        self.response.write(template.render(template_vars))
    def post(self):
        self.redirect("/")

class Home(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        all_people = User.query().fetch()
        if current_user:
            email_address = current_user.email()
            logout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/login'))
            self.response.write(" You're logged in as " + email_address + ". " + logout_link_html)
            is_existing_person = False
            for person in all_people:
                if person.email == email_address:
                    is_existing_person = True
            if (is_existing_person == False):
                new_user = User(
                    email=current_user.email(),
                    friends = [],
                    dates_free = [],
                )
                new_user.put()

            # get_current_user=User.query().filter(user.nickname() == User.email).get()
            template_vars = {
                "email_address": email_address,
            #     "friends": current_user.friends,
            }
        else:
            self.redirect("/login")
            template_vars = {}

        template = jinja_env.get_template('templates/home.html')
        self.response.write(template.render(template_vars))

class Profile(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        template_vars = {
            'current_user': current_user,
        }
        template = jinja_env.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))
    def post(self):
        current_user = users.get_current_user()
        get_current_user = User.query().filter(current_user.email() == User.email).get()
        user_free_date = self.request.get('user_free_date')
        get_current_user.dates_free.append(user_free_date)
        get_current_user.put()
        template_vars = {
            'date': user_free_date
        }
        template = jinja_env.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))

class Friends(webapp2.RequestHandler):
    def get(self):
        all_users = User.query().fetch()
        template_vars = {
            "all_users": all_users
        }
        template = jinja_env.get_template('templates/friends.html')
        self.response.write(template.render(template_vars))
    def post(self):
        current_user = users.get_current_user()
        get_current_user = User.query().filter(current_user.email() == User.email).get()
        all_people = User.query().fetch()
        for person in all_people:
            if_checked_person = self.request.get(person.email)
            if if_checked_person == "on":
                get_current_user.friends.append(person.key)
                get_current_user.put()

class Schedule(webapp2.RequestHandler):
    def get(self):
        template_vars = {
        }
        template = jinja_env.get_template('templates/schedule.html')
        self.response.write(template.render(template_vars))

    def post(self):
        current_user = users.get_current_user()
        get_current_user=User.query().filter(current_user.email() == User.email).get()
        hangout_date = self.request.get("hangout_date")
        friends_free = []
        if len(get_current_user.friends) != 0:
            for friend in get_current_user.friends:
                if len(friend.get().dates_free) != 0:
                    for date in friend.get().dates_free:
                        if hangout_date == date:
                            friends_free.append(friend.get().email)

        template_vars = {
            "hangout_date": hangout_date,
            "get_current_user": get_current_user,
            "friends_free": friends_free
        }
        template = jinja_env.get_template('templates/linkup.html')
        self.response.write(template.render(template_vars))


class populateDatabase(webapp2.RequestHandler):
    def get(self):
        alexa = User(
            first_name = 'Alexa',
            email = 'alexa@gmail.com',
            dates_free = ["2019-11-30", "2019-10-11", ],
            friends = []
        )
        alexa_key = alexa.put()

        ashlee = User(
            first_name = 'Ashlee',
            email = 'ashlee@example.com',
            dates_free = ["2019-11-30", "2019-12-11",],
            friends = []
        )
        ashlee_key = ashlee.put()

        alexa.friends = [ashlee_key]
        ashlee.friends = [alexa_key]

        alexa_key = alexa.put()
        ashlee_key = ashlee.put()

        self.redirect("/")

app=webapp2.WSGIApplication([
    ('/login', Login),
    ('/', Home),
    ('/profile', Profile),
    ('/friends', Friends),
    ('/schedule', Schedule),
    ('/populateDatabase', populateDatabase),
], debug=True)
