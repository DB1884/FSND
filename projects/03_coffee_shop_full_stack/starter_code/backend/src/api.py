from flask import Flask, request, jsonify
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, resources={r"/*": {"origins": "*"}})

db_drop_and_create_all()


# ROUTES
@app.route("/drinks", methods=["GET"])
def get_drinks():
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
    })


@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_detail(token):
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks]
    })


@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def post_drinks(token):
    drink_data = request.get_json()
    drink = Drink(
        title=drink_data.get("title"),
        recipe=json.dumps(drink_data.get("recipe")),
    )
    drink.insert()
    return jsonify({
        "success": True,
        "drinks": [drink.long()],
    })


@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patch_drinks(token, id):
    drink_data = request.get_json()
    drink = Drink.query.filter(Drink.id == id).first_or_404()
    drink.title = drink_data.get("title")
    drink.recipe = json.dumps(drink_data.get("recipe"))
    drink.update()
    return jsonify({
        "success": True,
        "drinks": [drink.long()],
    })


@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drinks(token, id):
    drink = Drink.query.filter(Drink.id == id).first_or_404()
    drink.delete()
    return jsonify({
        "success": True,
        "delete": drink.id,
    })


# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
        }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
        }), 404


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error["description"],
        }), error.status_code
