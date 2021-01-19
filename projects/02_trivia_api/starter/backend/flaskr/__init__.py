from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from models import Category, Question, setup_db
from sqlalchemy.sql.expression import func

QUESTIONS_PER_PAGE = 10


def get_questions(request, category_id=None, search_term=None):
    """Helper to get response for pages returning paginated question data"""
    if category_id:
        questions = Question.query.order_by(Question.id).filter(
            Question.category == category_id
        ).all()
        current_category = Category.query.filter(
            Category.id == category_id
        ).first_or_404()
    elif search_term:
        questions = Question.query.filter(
            Question.question.ilike(search_term)
        ).all()
        current_category = None
    else:
        questions = Question.query.order_by(Question.id).all()
        current_category = None

    all_categories = Category.query.all()

    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions]
    page_questions = questions[start:end]

    data = {
        "success": True,
        "questions": page_questions,
        "total_questions": len(questions),
        "categories": {
            category.id: category.type for category in all_categories
        },
        "current_category":
            current_category.format() if current_category else None
    }

    return data


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,DELETE")

        return response

    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable request"
        }), 422

    # Routes
    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()

        return jsonify({
            "success": True,
            "categories": {
                category.id: category.type for category in categories
            }
        })

    @app.route("/categories/<int:category_id>")
    def get_category(category_id):
        category = Category.query.filter(
            Category.id == category_id
        ).first_or_404()

        return jsonify({
            "success": True,
            "category": category.format()
        })

    @app.route("/categories/<int:category_id>/questions")
    def get_category_questions_paginated(category_id):
        questions_data = get_questions(request, category_id=category_id)
        if len(questions_data["questions"]) == 0:
            abort(404)

        return jsonify(questions_data)

    @app.route("/questions")
    def get_questions_paginated():
        questions_data = get_questions(request)
        if len(questions_data["questions"]) == 0:
            abort(404)

        return jsonify(questions_data)

    @app.route("/questions", methods=["POST"])
    def add_new_question():
        form_data = request.get_json()
        if any([not form_data[x] for x in form_data]):
            # Check for 'Falsey' values in form and return 400 in case of any
            abort(400)
        try:
            new_question = Question(
                question=form_data["question"],
                answer=form_data["answer"],
                difficulty=form_data["difficulty"],
                category=form_data["category"]
            )
            Question.insert(new_question)
        except Exception:
            abort(422)  # Return 422 if any field data is invalid

        return jsonify({
            "success": True
        })

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_book(question_id):
        question = Question.query.filter(
            Question.id == question_id
        ).first_or_404()
        question.delete()

        return jsonify({"success": True})

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        if not request.get_json()["searchTerm"]:
            abort(422)
        search_term = "%{}%".format(request.get_json()["searchTerm"])
        questions_data = get_questions(request, search_term=search_term)

        return jsonify(questions_data)

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        quiz_params = request.get_json()
        if quiz_params["quiz_category"]["id"] == 0:
            question = Question.query.order_by(func.random()).filter(
                Question.id.notin_(quiz_params["previous_questions"])
            ).first()
        else:
            question = Question.query.order_by(func.random()).filter(
                Question.category == quiz_params["quiz_category"]["id"],
                Question.id.notin_(quiz_params["previous_questions"])
            ).first()

        return jsonify({
            "success": True,
            "question": question.format() if question else None,
        })

    return app
