#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import jinja2
import webapp2
import jinja2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import users

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class Memory(ndb.Model):
    send_to= ndb.StringProperty(required=True)
    topic= ndb.StringProperty(required=True)
    content= ndb.TextProperty(required=True)
    delivery= ndb.DateTimeProperty(required=True)
    submit= ndb.DateTimeProperty(required=True, auto_now=True)

class MemoryHandler(webapp2.RequestHandler):
    def get(self):
         memory= Memory.query().fetch()
         memory.sort(key=lambda x:x.date, reverse=True)
         template= env.get_template("save.html")
         variables= {'posts': posts}
         self.response.write(template.render(variables))

    def post(self):
        title=self.request.get('title')
        content=self.request.get('content')
        post= Post(title=title,
                    content=content,
                    date=datetime.datetime.now())

        post.put()
        return self.redirect('/')

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            template = env.get_template('index.html')
            template_vars = {'logout': users.create_logout_url('/'),
                             'login': ('/login')}
            self.response.write(template.render(template_vars))
        else:
            self.redirect('/profile')

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user is None:
            login_url = users.create_login_url('/profile')
            # self.response.write('<a href="%s">Log In</a>' % login_url)
            self.redirect(login_url)

        # The user is logged in.
        else:
            self.redirect('/profile')
            # logout_url = users.create_logout_url('/')
            # self.response.write('Welcome, %s! ' % user.email())
            # self.response.write('<a href="%s">Log Out</a>' % logout_url)

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('save.html')
        self.response.write('Welcome, %s! ' % user.nickname())
        template_vars2 = {'logout': users.create_logout_url('/')}
        self.response.write(template.render(template_vars2))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/profile', ProfileHandler),

], debug=True)
