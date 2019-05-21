from flask import Flask

from goo_gl__2_0.config import BaseConfig

app = Flask(BaseConfig.PROJECT_NAME)
app.config['SECRET_KEY'] = BaseConfig.FLASK_SECRET_KEY
from goo_gl__2_0 import views
