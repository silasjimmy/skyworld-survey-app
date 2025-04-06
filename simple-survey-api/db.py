from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Text, Boolean, Enum, DateTime  # create_engine
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timezone

# SQLAlchemy database instance
db = SQLAlchemy()

database_path = "postgresql://{}:{}@{}/{}".format(
    'postgres', 'silas.jimmy.17', 'localhost:5432', 'sky_survey_db')


class GenderOptions(enum.Enum):
    """
    Gender options definition
    """

    male = 'MALE'
    female = 'FEMALE'
    other = 'OTHER'


class Question(db.Model):
    """
    A persistent question entity, extends the base SQLAlchemy Model
    """
    __tablename_ = 'question'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    required = Column(Boolean)
    text = Column(String)
    description = Column(String)
    options = relationship("Option")

    def __init__(self, name: str, type: str, required: bool, text: str, description: str):
        self.name = name
        self.type = type
        self.required = required
        self.text = text
        self.description = description

    def insert(self):
        """
        Saves the question information to the database
        """
        db.session.add(self)
        db.session.commit()

    def format(self):
        """
        Object representation of the Question model
        """
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'required': self.required,
            'text': self.text,
            'description': self.description
        }


class Response(db.Model):
    """
    A persistent response entity, extends the base SQLAlchemy Model
    """
    __tablename_ = 'response'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    email_address = Column(String, unique=True)
    description = Column(Text)
    date_responded = Column(DateTime, default=datetime.now(timezone.utc))
    gender = Column(String, Enum(GenderOptions))
    programming_stack = relationship("Option")
    certificates = relationship("Certificate")

    def __init__(self, full_name: str, email_address: str, description: str, gender: str):
        self.full_name = full_name
        self.email_address = email_address
        self.description = description
        self.gender = gender

    def insert(self):
        """
        Saves the response information to the database
        """
        db.session.add(self)
        db.session.commit()

    def format(self):
        """
        Object representation of the Response model
        """
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email_address': self.email_address,
            'description': self.description,
            'date_responded': self.date_responded,
            'gender': self.gender
        }


class Option(db.Model):
    """
    A persistent option entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    value = Column(String)

    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value

    def insert(self):
        """
        Saves the option information to the database
        """
        db.session.add(self)
        db.session.commit()

    def format(self):
        """
        Object representation of the Option model
        """
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value
        }


class Certificate(db.Model):
    """
    A persistent certificate entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'certificate'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def insert(self):
        """
        Saves the certificate information to the database
        """
        db.session.add(self)
        db.session.commit()

    def format(self):
        """
        Object representation of the Option model
        """
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }


def setup_database(app: object, database_path: str = ''):
    """
    Connects the database to the Flask application.

    :param app: Flask application context
    :param database_path: Path to the database
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
