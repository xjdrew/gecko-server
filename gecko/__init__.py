import datetime

from flask import Flask

app = Flask(__name__)
logger = app.logger
app.secret_key = '(\x1c\x94\xde{\x9b\x90m\xee\xc2\x90\xfc\xde\x05\xcf\x10\xf3\x96ww\xf0*\xbf{'
app.permanent_session_lifetime = datetime.timedelta(seconds=3600*8)

import gecko.views

