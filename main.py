import webapp2
import logging
import jinja2
import os
import json
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import search
from urlparse import urlparse
from datetime import date


jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class APIKey(ndb.Model):
    api_key = ndb.StringProperty(required=True)

api_key = APIKey.query().fetch()[0].api_key

class Profile(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()
    dates_free = ndb.StringProperty(repeated=True)
    friends = ndb.KeyProperty(repeated=True, kind='Profile')

def get_current_email():
    return users.get_current_user()

def get_current_profile():
    current_user = get_current_email()
    return Profile.query().filter(current_user.email() == Profile.email).get()

def get_all_profiles():
    return Profile.query().fetch()

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
        key_query_parameter = self.request.get('key_query_parameter')
        current_user = get_current_email()
        all_people = get_all_profiles()

        if current_user:
            email_address = current_user.email()
            logout_link = users.create_logout_url('/login')
            is_existing_person = False
            for person in all_people:
                if person.email == email_address:
                    is_existing_person = True

            if (is_existing_person == False):
                new_user = Profile(
                    email=current_user.email(),
                    friends = [],
                    dates_free = [],
                )
                new_user.put()
                template = jinja_env.get_template('templates/registration.html')
                self.response.write(template.render())

            else:
                user_free_dates = sorted(get_current_profile().dates_free)
                friend_list = get_current_profile().friends
                if key_query_parameter != "":
                    first_name = key_query_parameter
                else:
                    first_name = get_current_profile().first_name
                template_vars = {
                    "first_name": first_name,
                    "user_free_dates": user_free_dates,
                    "logout_link": logout_link,
                    "friend_list": friend_list
                }
                template = jinja_env.get_template('templates/home.html')
                self.response.write(template.render(template_vars))

        else:
            self.redirect("/login")

    def post(self):
        current_user = get_current_email()
        get_current_user = get_current_profile()
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        get_current_user.first_name = first_name
        get_current_user.last_name = last_name
        get_current_user.put()
        self.redirect('/?key_query_parameter=%s' % first_name)

class EditProfile(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        get_current_user = get_current_profile()
        added_dates = sorted(get_current_user.dates_free)
        template_vars = {
        'current_user': current_user,
        'added_dates': added_dates,
        }

        if get_current_user.dates_free:
            template_vars = {
                'current_user': current_user,
                'added_dates': added_dates,
            }
        else:
            template_vars = {
            'current_user': current_user,
            'added_dates': added_dates,
            }
        template = jinja_env.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))

    def post(self):
        request_dictionary = json.loads(self.request.body)
        current_user = users.get_current_user()
        get_current_user = get_current_profile()
        result = False
        if 'user_free_date' in request_dictionary.keys():
            user_free_date = request_dictionary['user_free_date']
            if user_free_date not in get_current_user.dates_free:
                get_current_user.dates_free.append(user_free_date)
                get_current_user.put()
                result = True
        if 'date_removed' in request_dictionary.keys():
            remove_date = request_dictionary['date_removed']
            get_current_user.dates_free.remove(remove_date)
            get_current_user.put()
        added_dates = sorted(get_current_user.dates_free)
        jsonResponseData = {
            'status': result,
            'added_dates': added_dates,
        }
        self.response.write(json.dumps(jsonResponseData))

class Friends(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        get_current_user = get_current_profile()
        all_users = Profile.query().filter(current_user.email() != Profile.email).fetch()
        template_vars = {
            "all_users": all_users,
            'get_current_user': get_current_user
        }
        template = jinja_env.get_template('templates/friends.html')
        self.response.write(template.render(template_vars))
    def post(self):
        current_user = get_current_email()
        all_users = Profile.query().filter(current_user.email() != Profile.email).fetch()
        get_current_user = get_current_profile()
        search = self.request.get('search') #User Input Search
        searched_friends_first = Profile.query().filter(Profile.first_name == search).fetch()
        searched_friends_last = Profile.query().filter(Profile.last_name == search).fetch()
        searched_friends_email = Profile.query().filter(Profile.email == search).fetch()
        searched_friends = []
        template_vars = {
                "all_users": all_users,
                'get_current_user': get_current_user,
        }

        if not searched_friends_first:
            if not searched_friends_last:
                if searched_friends_email:
                    searched_friends.extend(searched_friends_email)
            else:
                searched_friends.extend(searched_friends_last)
        else:
            searched_friends.extend(searched_friends_first)
        template_vars["searched_friends"]=searched_friends
        template_vars["results"]="Here are your results: "

        for person in all_users:
            if_checked_person = self.request.get(person.email)
            if if_checked_person == "on":
                get_current_user.friends.append(person.key)
                get_current_user.put()
        template = jinja_env.get_template('templates/friends.html')
        self.response.write(template.render(template_vars))

class Schedule(webapp2.RequestHandler):
    def get(self):
        template_vars = {
        }
        template = jinja_env.get_template('templates/schedule.html')
        self.response.write(template.render(template_vars))

    def post(self):
        current_user = get_current_email()
        get_current_user=get_current_profile()
        hangout_date = self.request.get("hangout_date")
        city = self.request.get("city")
        friends_free = []
        if len(get_current_user.friends) != 0:
            for friend in get_current_user.friends:
                if len(friend.get().dates_free) != 0:
                    for date in friend.get().dates_free:
                        if hangout_date == date:
                            friends_free.append(friend.get().first_name)

        template_vars = {
            "hangout_date": hangout_date,
            "get_current_user": get_current_user,
            "friends_free": friends_free,
            'api_key': api_key,
            'city': city,
        }
        template = jinja_env.get_template('templates/linkup.html')
        self.response.write(template.render(template_vars))

class populateDatabase(webapp2.RequestHandler):
    def get(self):
        alexa = Profile(
            first_name = 'Alexa',
            last_name = 'Ramirez',
            email = 'alexa@gmail.com',
            dates_free = ["2019-11-30", "2019-10-11",],
            friends = []
        )
        alexa_key = alexa.put()

        ashlee = Profile(
            first_name = 'Ashlee',
            last_name = 'Kupor',
            email = 'ashlee@example.com',
            dates_free = ["2019-11-30", "2019-12-11",],
            friends = []
        )
        ashlee_key = ashlee.put()

        sydney = Profile(
            first_name = 'sydney',
            last_name = 'Martinez',
            email = 'sydney@example.com',
            dates_free = ["2019-11-30", "2019-12-11",],
            friends = []
        )
        sydney_key = sydney.put()

        alexa.friends = [ashlee_key]
        ashlee.friends = [alexa_key]
        sydney.friends = [alexa_key]

        alexa_key = alexa.put()
        ashlee_key = ashlee.put()
        sydney_key = sydney.put()

        self.redirect("/")

app=webapp2.WSGIApplication([
    ('/login', Login),
    ('/', Home),
    ('/profile', EditProfile),
    ('/friends', Friends),
    ('/schedule', Schedule),
    ('/populateDatabase', populateDatabase),
], debug=True)
