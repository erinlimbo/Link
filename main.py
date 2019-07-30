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
    nickname = ndb.StringProperty()
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
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            logout_link_html = '<a href="%s">sign out</a>' % (users.create_logout_url('/login'))
            self.response.write(" You're logged in as " + email_address + ". " + logout_link_html)
            current_user = User(
                nickname=user.nickname(),
                email=user.email(),)
            current_user.put()
        else:
            self.redirect("/login")

        template_vars = {
            "email_address": email_address,
        }
        template = jinja_env.get_template('templates/home.html')
        self.response.write(template.render(template_vars))

    def post(self):
        current_user = users.get_current_user()
        user = User(
            nickname=current_user.nickname(),
            email=current_user.email(),
        )
        user.put()
        self.response.write('Thanks for signing up, %s! <br><a href="/">Home</a>' %
            user.first_name)
        self.redirect("/")

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
        get_current_user = User.query().filter(current_user.nickname() == User.email).fetch()
        user_free_date = self.request.get('user_free_date')
        # date_list = get_current_user[0].dates_free
        get_current_user[0].dates_free.append(user_free_date)
        print get_current_user[0].dates_free
        print user_free_date
        print "hello"

        # dates_free.append(free_date)
        template_vars = {
            'date': user_free_date
        }
        template = jinja_env.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))

class Friends(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        get_current_user=User.query().filter(current_user.nickname() == User.email).fetch()
        # for friend in get_current_user[0].friends:
        #             friends_free.append(friend.get().email)
        # ancestor_key = ndb.Key('email', "sydneym2019@gmail.com")
        template_vars = {
            "friends": get_current_user[0].friends
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
        current_user = users.get_current_user()
        get_current_user=User.query().filter(current_user.nickname() == User.email).fetch()
        hangout_date = self.request.get("hangout_date")
        friends_free = []
        for friend in get_current_user[0].friends:
            for date in friend.get().dates_free:
                if hangout_date == date:
                    friends_free.append(friend.get().email)

        template_vars = {
            "hangout_date": hangout_date,
            "get_current_user": get_current_user[0],
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
