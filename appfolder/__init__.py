from flask import Flask

appFlask = Flask(__name__)
appFlask.config['SECRET_KEY'] = 'something-super-secret'

from appfolder import routes
