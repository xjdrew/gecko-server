import datetime, os
from flask import Flask

app = Flask(__name__)

# config ca
ca_folder = 'ca'
app.config["PRIVATE_KEY"] = os.path.join(ca_folder, 'wodaole.key')
app.config["SIGNER"] = os.path.join(ca_folder, 'wodaole.crt')
app.config["CERTIFICATE"] = os.path.join(ca_folder, "PositiveSSLCA2.crt")
app.config["MC_NAME"] = "gecko"
app.config["MC_IDENTIFIER"] = "com.wodaole.vpn"

assert os.path.exists(app.config["PRIVATE_KEY"])
assert os.path.exists(app.config["SIGNER"])
assert os.path.exists(app.config["CERTIFICATE"])

logger = app.logger
app.secret_key = '(\x1c\x94\xde{\x9b\x90m\xee\xc2\x90\xfc\xde\x05\xcf\x10\xf3\x96ww\xf0*\xbf{'
app.permanent_session_lifetime = datetime.timedelta(seconds=3600*8)

import gecko.views

