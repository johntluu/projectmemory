
from google.appengine.ext.webapp.util import run_wsgi_app
import jinja2
import webapp2
import logging


class ScheduledTaskHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("RESPONSE!!!!!!!!")
        logging.info("hello world")

application = webapp2.WSGIApplication([('/cron', ScheduledTaskHandler)],
                                     debug=True)
if __name__ == '__main__':
    run_wsgi_app(application)
