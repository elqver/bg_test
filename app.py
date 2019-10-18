from flask import Flask
from server_config import Config

app = Flask(__name__)
app.config.from_object(Config)
