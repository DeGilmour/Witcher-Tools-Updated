from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os, sys
from flask_bootstrap import Bootstrap

template_dir = os.path.abspath('loot_generator/html/')
static_folder = os.path.abspath('loot_generator/static/')
app = Flask(__name__,  template_folder=template_dir)
Bootstrap(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from loot_generator.model import loot_generator_model
from loot_generator.controller import loot_generator_controller
from loot_generator.controller import combat_simulator
