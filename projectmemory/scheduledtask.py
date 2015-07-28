from google.appengine.ext import webapp2
from google.appengine.ext.webapp2.util import run_wsgi_app
import jinja2
import webapp2

class ScheduledTaskHandler(webapp2.RequestHandler):
    def get(self):
        print "hello world"

application = webapp.WSGIApplication([('/cron', ScheduledTaskHandler)],
                                     debug=True)
if __name__ == '__main__':
    run_wsgi_app(application)
