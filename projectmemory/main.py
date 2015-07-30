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
import logging
import webapp2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.api import mail

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class Memory(ndb.Model):
    current_user= ndb.StringProperty(required=True)
    send_to= ndb.StringProperty(required=True)
    subject= ndb.StringProperty(required=True)
    content= ndb.TextProperty(required=True)
    delivery= ndb.DateProperty(required=True)
    attachment=ndb.BlobProperty()
    date= ndb.DateProperty(required=True, auto_now=True)


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
            self.redirect('/')
            # logout_url = users.create_logout_url('/')
            # self.response.write('Welcome, %s! ' % user.email())
            # self.response.write('<a href="%s">Log Out</a>' % logout_url)

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('profile.html')
        posts= Memory.query(Memory.current_user == user.email()).fetch()
        posts.sort(key=lambda x:x.date, reverse=True)
        self.response.write('Welcome, %s! ' % user.nickname())
        template_vars2 = {'logout': users.create_logout_url('/'), 'posts': posts}
        self.response.write(template.render(template_vars2))
    def post(self):
        user = users.get_current_user()
        current_user_var= user.email()
        subject_var=self.request.get('subject')
        content_var=self.request.get('content')
        send_to_var=self.request.get('send_to')
        attachment_var=self.request.get('attachment')
        delivery_var= datetime.datetime.strptime(self.request.get('delivery'), '%Y-%m-%d')
        post= Memory(subject=subject_var,
                   content=content_var,
                   date=datetime.datetime.today(),
                   send_to=send_to_var,
                   delivery=delivery_var,
                   current_user=current_user_var,
                   attachment=attachment_var)
        post.put() # stores info in the database
        return self.redirect('/')

class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template= env.get_template('profile.html')
        rowkey= ndb.Key(urlsafe=self.request.get("delete"))
        rowkey.delete()
        posts= Memory.query(Memory.current_user == user.email()).fetch()
        self.response.write('Welcome, %s! ' % user.nickname())
        template_vars2 = {'logout': users.create_logout_url('/'), 'posts': posts}
        self.response.write(template.render(template_vars2))
        return self.redirect('/profile')



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/profile', ProfileHandler),
    ('/delete', DeleteHandler),

], debug=True)
