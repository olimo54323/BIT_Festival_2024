from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .question import Question
from .result import Result
from .category import Category
from .hobby import Hobby
