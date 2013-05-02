import time, base64, json, os
from datetime import datetime

from flask import make_response, safe_join, session
from gecko import app, logger
from auth import auth
import dbhelper, mcsign, mc


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
def index():
    content = ''
    public_crt = safe_join(app.config['CA_FOLDER'], 'wodaole.crt')
    with open(public_crt) as f:
        content = f.read()
        
    r = dict(greeting='hello world',
             time=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
             pwd=os.getcwd(),
             signer = content)
    return make_json_response(r)


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
    return make_json_response(dbhelper.get_all_server_profile())

@app.route('/user/<user>/<token>/<param>/')
def mobileconfig(user, token, param):
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

@app.route('/user/<int:sid>')
def mobileconfig_test(sid):
    sids = [1,2,3]
    configs = []
    for sid in sids:
        configs.append(dbhelper.get_server_config(sid))

    mobileconfig = mc.get_mobileconfig(configs)
    resp = make_response(mcsign.sign(mobileconfig))
    resp.headers['Content-type'] = 'application/x-apple-aspen-config; charset=utf-8'
    resp.headers['Content-Disposition'] = 'attachment; filename="test.mobileconfig"'
    return resp
