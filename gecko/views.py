from datetime import datetime
import time, base64, json

from flask import make_response, session

from gecko import app, logger
from auth import auth
import dbhelper


def error_string(code):
    err_tbl = {}
    err_tbl[0] = "success"
    return err_tbl[code]


def make_json_response(data, code=0):
    ret = dict(code=code, reason=error_string(code))
    js = json.dumps(dict(ret=ret, data=data), indent=4)
    response = make_response(js)
    response.mimetype = "application/json"
    return response


@app.route('/')
@auth.requires_auth
def index():
    r = dict(greeting='hello world',
             time=datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

    resp = make_response(json.dumps(r, indent=4))
    resp.mimetype = "application/json"
    resp.set_cookie('username', 'the name')
    return resp


@app.route('/login/')
@auth.requires_auth
def login():
    return make_json_response(None)

@app.route('/profile/')
@auth.requires_auth
def profile():
    user = dbhelper.get_user_profile(session['username'])
    return make_json_response(user)

@app.route('/vpnservers/')
@auth.requires_auth
def server_list():
    data = []
    data.append(dict(sid=1, name="us-01", country="us", ip="127.0.0.1"))
    data.append(dict(sid=2, name="us-02", country="us", ip="127.0.0.1"))
    data.append(dict(sid=3, name="us-03", country="us", ip="127.0.0.1"))
    data.append(dict(sid=4, name="us-04", country="us", ip="127.0.0.1"))
    data.append(dict(sid=5, name="hk-01", country="hk", ip="127.0.0.1"))
    data.append(dict(sid=6, name="hk-02", country="hk", ip="127.0.0.1"))
    data.append(dict(sid=7, name="cn-01", country="cn", ip="127.0.0.1"))
    logger.debug(data)
    return make_json_response(data)

@app.route('/user/<user>/<token>/<param>/')
def file(user, token, param):
    if not auth.is_token_valid(user, token, param):
        return make_response("Forbidden: unrecognized user token", 403)
    param = param.encode("utf-8")
    sids = json.loads(base64.urlsafe_b64decode(param))
    logger.debug("mobileconfig: %s", str(sids))

    with app.open_resource('signed.mobileconfig') as f:
        resp = make_response(f.read())
        # resp.headers['Content-type'] = 'application/octet-stream'
        resp.headers['Content-type'] = 'application/x-apple-aspen-config; charset=utf-8'
        resp.headers['Content-Disposition'] = 'attachment; filename="test.mobileconfig"'
    return resp
