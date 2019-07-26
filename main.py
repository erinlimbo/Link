import webapp2
import logging
import jinja2
import os

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("Link")
        template_vars = {
        
        }

        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render(template_vars))

app=webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
