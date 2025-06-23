from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .client import *
from .contact import *
from .client_contact import *
from .user import *