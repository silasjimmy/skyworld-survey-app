from flask import Flask, jsonify, abort, request
from database.models import database, setup_database, Question, Response, Certificate, Option
from flask_cors import CORS
from flask_swagger import swagger
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    with app.app_context():
        setup_database(app)

    # Set up cors and allowed * origins
    CORS(app, resources={r"/api/*": {'origins': "*"}})

    Migrate(app, database)

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

    @app.route('/api/questions/responses')
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

    @app.route('/api/questions/responses/certificates/<int:certificate_id>')
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

    @app.route('/api/questions/question', methods=['PUT'])
    def add_question():
        """
        Save a survey question
        ---
        tags:
          - question
        responses:
          200:
            description: question uploaded successfully
        """
        try:
            question_data = request.form.to_dict()

            if question_data.get('options'):
                # Create a list of option ids from the provided string
                question_options = question_data.get('options').split(',')

                # Convert the string ids to integers
                option_ids = [int(question_id)
                              for question_id in question_options]

                # Create Option entities from the generated ids
                options = [Option.query.filter_by(
                    id=option_id).one_or_none() for option_id in option_ids]

                # Remove None values from the list, if any
                question_data['options'] = list(
                    filter(lambda o: o is not None, options))

            # Convert the 'required' value to a boolean value
            question_data['required'] = bool(question_data.get('required'))

            new_question = Question(**question_data)
            new_question.insert()

            return jsonify({
                "status": 200,
                "success": True,
                "question": new_question.format()
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/api/questions/options', methods=['PUT'])
    def add_option():
        """
        Save a question option
        ---
        tags:
          - option
        responses:
          200:
            description: option uploaded successfully
        """
        try:
            option_data = request.form.to_dict()

            new_option = Option(**option_data)
            new_option.insert()

            return jsonify({
                "status": 200,
                "success": True,
                "otion": new_option.format()
            })
        except Exception as e:
            print(e)
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

            new_response = Response(**response_data.to_dict())

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
