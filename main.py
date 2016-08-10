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
import os
import webapp2
import random
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class User(ndb.Model):
    name = ndb.StringProperty()
    comment = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user_query = User.query()
        user_query = user_query.order(-User.time)
        user_data = user_query.fetch(10)
        template_params = {}
        template_params['users'] = user_data
        template = JINJA_ENVIRONMENT.get_template('shoutbox.html')
        self.response.write(template.render(template_params))

    def post(self):
        name = self.request.get('name')
        if len(name) == 0:
            name = "Anonymous"
        comment = self.request.get('comment')
        user = User(name=name, comment=comment)
        user.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
