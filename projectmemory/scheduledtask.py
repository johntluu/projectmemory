
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
import webapp2
import logging
import datetime
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.api import users
from main import Memory


# class Memory(ndb.Model):
#     current_user= ndb.StringProperty(required=True)
#     send_to= ndb.StringProperty(required=True)
#     subject= ndb.StringProperty(required=True)
#     content= ndb.TextProperty(required=True)
#     delivery= ndb.DateProperty(required=True)
#     date= ndb.DateProperty(required=True, auto_now=True)
#     attachment=ndb.BlobProperty()

class ScheduledTaskHandler(webapp2.RequestHandler):
    def get(self):
        currentdate = datetime.datetime.today()
        datetoday = datetime.datetime(year=currentdate.year, month=currentdate.month, day=currentdate.day)
        # datetimetoday = datetime.datetime.today()
        memories = Memory.query(Memory.delivery == datetoday).fetch()
        # logging.info(datetoday)
        # logging.info(var)

        # mail function
        # user = users.get_current_user()
        for memory in memories:
            if memory.attachment:
                mail.send_mail(sender="%s" % "memory.delivery@project-memory.appspotmail.com",
                               to= memory.send_to,
                               subject="You have a Memory from " + str(memory.current_user) + ": " + str(memory.subject),
                               body= memory.content,
                               attachments=[("yourattachment", memory.attachment)])
            else:
                mail.send_mail(sender="%s" % "memory.delivery@project-memory.appspotmail.com",
                               to= memory.send_to,
                               subject="You have a Memory from " + str(memory.current_user) + ": " + str(memory.subject),
                               body= memory.content)


application = webapp2.WSGIApplication([('/cron', ScheduledTaskHandler)],
                                     debug=True)
if __name__ == '__main__':
    run_wsgi_app(application)
