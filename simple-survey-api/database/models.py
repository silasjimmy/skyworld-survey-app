from sqlalchemy import Column, String, Integer, Text, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime, timezone
from utils import GenderOptions
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy database instance
database = SQLAlchemy()

database_path = "postgresql://{}:{}@{}/{}".format(
    'postgres', 'silas.jimmy.17', 'localhost:5432', 'sky_survey_db')


def setup_database(app: object, database_path: str = database_path):
    """
    Connects the database to the Flask application.

    :param app: Flask application context
    :param database_path: Path to the database
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    database.app = app
    database.init_app(app)
    database.create_all()


#############
### Models###
#############


class Question(database.Model):
    """
    A persistent question entity, extends the base SQLAlchemy Model
    """
    __tablename_ = 'question'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    required = Column(Boolean, nullable=False)
    text = Column(String, nullable=False)
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
        database.session.add(self)
        database.session.commit()

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


class Response(database.Model):
    """
    A persistent response entity, extends the base SQLAlchemy Model
    """
    __tablename_ = 'response'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email_address = Column(String, unique=True, nullable=False) # Enforce `unique` to avoid multiple entries
    description = Column(Text, nullable=False)
    gender = Column(String, Enum(GenderOptions), nullable=False)
    date_responded = Column(DateTime, default=datetime.now(timezone.utc))
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
        database.session.add(self)
        database.session.commit()

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


class Option(database.Model):
    """
    A persistent option entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'option'

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    value = Column(String, nullable=False)
    question_id = mapped_column(ForeignKey("question.id"))
    response_id = mapped_column(ForeignKey("response.id"))

    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value

    def insert(self):
        """
        Saves the option information to the database
        """
        database.session.add(self)
        database.session.commit()

    def format(self):
        """
        Object representation of the Option model
        """
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value
        }


class Certificate(database.Model):
    """
    A persistent certificate entity, extends the base SQLAlchemy Model
    """
    __tablename__ = 'certificate'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    response_id = mapped_column(ForeignKey("response.id"))

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    def insert(self):
        """
        Saves the certificate information to the database
        """
        database.session.add(self)
        database.session.commit()

    def format(self):
        """
        Object representation of the Option model
        """
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }
