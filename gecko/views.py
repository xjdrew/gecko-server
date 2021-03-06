import time, base64, json, os, httplib, urllib2
from datetime import datetime

from flask import make_response, safe_join, session, request
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

    r = dict(greeting='hello world',
             time=datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
             pwd=os.getcwd())
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

    configs = []
    for sid in sids:
        configs.append(dbhelper.get_server_config(sid))

    mobileconfig = mc.get_mobileconfig(configs)
    resp = make_response(mcsign.sign(mobileconfig))
    resp.headers['Content-type'] = 'application/x-apple-aspen-config; charset=utf-8'
    resp.headers['Content-Disposition'] = 'attachment; filename="%s.mobileconfig"' % app.config["MC_NAME"]
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
    resp.headers['Content-Disposition'] = 'attachment; filename="%s.mobileconfig"' % app.config["MC_NAME"]
    return resp

@app.route('/purchase', methods=['POST'])
def purchase():
    receipt = request.json['receipt']
    logger.debug("receipt: %s", type(receipt))

    req = {"receipt-data" : receipt}
    data = json.dumps(req)

    url = "https://sandbox.itunes.apple.com/verifyReceipt"
    headers = {'Content-Type' : 'application/json'}
    handler = urllib2.urlopen(url, data)
    logger.debug("verify receipt code: %d", handler.code)
    logger.debug("verify receipt: %s", handler.read())
    return make_json_response('')
