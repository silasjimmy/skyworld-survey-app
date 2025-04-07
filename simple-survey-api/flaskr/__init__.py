from flask import Flask, jsonify
from database.models import setup_database
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)

    with app.app_context():
        setup_database(app)

    # Set up cors and allowed * origins
    CORS(app, resources={r"/api/*": {'origins': "*"}})

    # Access the after request to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    @app.route('/')
    def home():
        return 'Sky World Survey App!'

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "request could not be processed"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "internal server error"
        }), 500

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request error"
        }), 400

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "record not found"
        }), 404

    return app
