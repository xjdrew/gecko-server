import time, hmac, base64
from functools import wraps
from flask import request, session, make_response

import authdigest, dbhelper
from gecko import logger


class FlaskRealmDigestDB(authdigest.RealmDigestDB):
    cookie_interval = 60 * 60 * 8

    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not self.is_logined():
                if not self.isAuthenticated(request):
                        return self.challenge()
                session.permanent = False
                session['username'] = request.authorization.username
            return f(*args, **kwargs)

        return decorated

    def is_token_valid(self, user, token, param):
        """
        for download mobileconfig file
        """
        password = self.get_password(user)
        if not password:
            return False

        mac = hmac.new(password)
        mac.update(user)
        mac.update(param)
        # return make_response("Forbidden: unrecognized user token", 403)
        return token == base64.urlsafe_b64encode(mac.digest())

    def is_logined(self):
        if 'username' in session:
            return True
        return False

    def get_password(self, user):
        return dbhelper.get_password(user)

auth = FlaskRealmDigestDB('MyAuthRealm')
