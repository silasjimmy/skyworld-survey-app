from flask import Flask, jsonify, abort, request
from database.models import setup_database, Question, Response, Certificate
from flask_cors import CORS
from flask_swagger import swagger


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
                             'GET, PUT')
        return response

    @app.route('/')
    def docs():
        """
        API Documentation with Swagger
        ---
        tags:
          - docs
        responses:
          200:
            description: documentation retrieved successfully
        """
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Sky Survey API"
        return jsonify({
            "status": 200,
            "success": True,
            "docs": swag
        })

    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        """
        Get a list of all survey questions
        ---
        tags:
          - questions
        responses:
          200:
            description: questions retrieved successfully
        """
        try:
            questions_query = Question.query.all()

            questions = [question.format() for question in questions_query]

            return jsonify({
                "status": 200,
                "success": True,
                "questions": questions
            })
        except Exception as e:
            abort(422)

    @app.route('/api/questions/responses', methods=['GET'])
    def get_responses():
        """
        Get a list of all survey responses
        ---
        tags:
          - responses
        responses:
          200:
            description: responses retrieved successfully
        """
        try:
            responses_query = Response.query.all()

            responses = [response.format() for response in responses_query]

            return jsonify({
                "status": 200,
                "success": True,
                "responses": responses
            })
        except Exception as e:
            abort(422)

    @app.route('/api/questions/responses/certificates/<int:certificate_id>', methods=['GET'])
    def get_certificate(certificate_id):
        """
        Get a survey response certificate by id
        ---
        tags:
          - certificate
        responses:
          200:
            description: certificate retrieved successfully
        """
        try:
            certificate = Certificate.query.filter(
                Certificate.id == certificate_id).one_or_none()

            return jsonify({
                "status": 200,
                "success": True,
                "certificate": certificate
            })
        except Exception as e:
            abort(422)

    @app.route('/api/questions/responses', methods=['PUT'])
    def add_response():
        """
        Save a user survey response
        ---
        tags:
          - response
        responses:
          200:
            description: responses uploaded successfully
        """
        try:
            response_data = request.form

            # response_files = request.files
            # print(response_files)

            new_response = Response(**response_data)

            return jsonify({
                "status": 200,
                "success": True,
                "response": new_response.format()
            })
        except Exception as e:
            abort(422)

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
