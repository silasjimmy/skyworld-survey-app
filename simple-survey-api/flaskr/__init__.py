from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def home():
        return 'Sky World Survey App!'

    return app