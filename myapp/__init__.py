from configparser import ConfigParser

from myapp.libs.Task import Task

from flask import Flask
from myapp.api import api_bp
from werkzeug.utils import import_string


def create_app(confpath:str):

    conf = ConfigParser()
    conf.read(confpath)
    
    # task = Task(conf.get("data","mf4txtpath"),conf.get("data","imgoutput"))
    # task.run(timesnumber=2).start() # 开启后台执行

    app = Flask(__name__)
    
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
