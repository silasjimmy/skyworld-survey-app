import enum
from os.path import join, dirname, realpath

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/certificates')
ALLOWED_EXTENSIONS = ['pdf']


class GenderOptions(enum.Enum):
    """
    Gender options definition
    """

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'


def allowed_file(filename: str):
    """
    Checks if the uploaded file is among the allowed files
    
    Parameters:
        filename (str): name of the uploaded file
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
