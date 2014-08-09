#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2012, Dongsheng Cai
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Dongsheng Cai nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL DONGSHENG CAI BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from hashlib import md5, sha1
from routes import route
from tornado.options import options
import logging
import os
import platform
import random
import tornado.web
from bson.objectid import ObjectId
import time
import uuid
from constants import DEVICE_TYPE_IOS, VERSION
from pymongo import DESCENDING
from util import filter_alphabetanum
from pushservices.apns import APNClient, APNFeedback, PayLoad
import sys
from api import API_PERMISSIONS
from pushservices.gcm import GCMException
from pushservices.wns import WNSClient
from pushservices.gcm import GCMClient
import requests
from controllers.base import *

@route(r"/auth/([^/]+)")
class AuthHandler(WebBaseHandler):
    def get(self, action):
        next = self.get_argument('next', "/")
        if action == 'logout':
            self.clear_cookie('user')
            self.redirect(next)
        else:
            self.render('login.html')

    def post(self, action):
        next = self.get_argument('next', "/")
        if action == 'logout':
            self.clear_cookie('user')
        else:
            username = self.get_argument('username', None)
            password = self.get_argument('password', None)
            passwordhash = sha1("%s%s" % (options.passwordsalt, password)).hexdigest()
            user = self.masterdb.managers.find_one({'username': username, 'password': passwordhash})
            if user:
                self.set_secure_cookie('user', str(user['_id']))
        self.redirect(next)