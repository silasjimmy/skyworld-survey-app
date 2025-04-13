from flask import Flask, jsonify, abort, request, send_from_directory
from database.models import database, setup_database, Question, Response, Certificate, Option
from flask_cors import CORS
from flask_swagger import swagger
from flask_migrate import Migrate
from dotenv import load_dotenv
from utils import UPLOAD_FOLDER, allowed_file
from werkzeug.utils import secure_filename
import os
from typing import List, Dict

# Load environment variables
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * \
        1000  # Maximum size of 1MB per file

    # Create the static/certificates folder if it does not exists
    try:
        os.makedirs(UPLOAD_FOLDER)
    except OSError:
        pass

    # Initialize the database
    with app.app_context():
        setup_database(app)

    # Set up cors and allowed * origins
    CORS(app, resources={r"/api/*": {'origins': "*"}})

    # Set up migrations
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
            certificate: Certificate = Certificate.query.filter(
                Certificate.id == certificate_id).one_or_none()

            if certificate:
                return send_from_directory(app.config["UPLOAD_FOLDER"], certificate.name)
            else:
                abort(404)
        except Exception as e:
            print(e)
            abort(422)

    # Mark for deletion
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

    # Mark for deletion
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

        # Abort if no certificates uploaded
        if 'certificates' not in request.files:
            abort(422)

        uploaded_certificates = request.files.getlist('certificates')

        # Check for empty files
        if '' in [certificate.filename for certificate in uploaded_certificates]:
            abort(404)

        try:
            response_certificates: List[Dict[str, str]] = []

            # Save the uploaded certificates
            for certificate in uploaded_certificates:
                if certificate and allowed_file(certificate.filename):
                    filename = secure_filename(certificate.filename)
                    certificate.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))
                    response_certificates.append({
                        'name': filename,
                        'url': filename
                    })

            response_data = request.form.to_dict()

            new_response = Response(**response_data)
            new_response.certificates = [
                Certificate(name=certificate.get('name'),
                            url=certificate.get('url'))
                for certificate in response_certificates]

            new_response.insert()

            return jsonify({
                "status": 200,
                "success": True,
                "response": new_response.format()
            })
        except Exception as e:
            print(e)
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
