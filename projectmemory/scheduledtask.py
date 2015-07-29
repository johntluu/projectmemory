
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
import webapp2
import logging
import datetime
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.api import users


class Memory(ndb.Model):
    current_user= ndb.StringProperty(required=True)
    send_to= ndb.StringProperty(required=True)
    subject= ndb.StringProperty(required=True)
    content= ndb.TextProperty(required=True)
    delivery= ndb.DateProperty(required=True)
    date= ndb.DateProperty(required=True, auto_now=True)

class ScheduledTaskHandler(webapp2.RequestHandler):
    def get(self):
        currentdate = datetime.datetime.today()
        datetoday = datetime.datetime(year=currentdate.year, month=currentdate.month, day=currentdate.day)
        # datetimetoday = datetime.datetime.today()
        var = Memory.query(Memory.delivery == datetoday).fetch()
        # logging.info(datetoday)
        # logging.info(var)

        # mail function
        # user = users.get_current_user()
        if var:
            for result in var:

                mail.send_mail(sender="%s" % "memory.delivery@project-memory.appspotmail.com",
                               to= result.send_to,
                               subject="You have a Memory from " + str(result.current_user) + ": " + str(result.subject),
                               body= result.content)


application = webapp2.WSGIApplication([('/cron', ScheduledTaskHandler)],
                                     debug=True)
if __name__ == '__main__':
    run_wsgi_app(application)
