import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()


@app.route('/drinks')
def get_drinks():
    """ Get drinks from the database """
    try:
        drinks = Drink.query.all()
        formatted_drinks = [drink.short() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': formatted_drinks
        })
    except Exception as e:
        print(f'Error occurred in get_drinks(): {e}')
        abort(422)


@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drink_detail(jwt):
    """ Get drink details from the database """

    try:
        drinks = Drink.query.all()
        formatted_drinks = [drink.long() for drink in drinks]

        return jsonify({
            'success': True,
            'drinks': formatted_drinks
        })
    except Exception as e:
        print(f'Error occurred in get_drink_detail(): {e}')
        abort(422)


@app.route("/drinks", methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    """ Create a drink in the database """

    body = request.get_json()

    if not ('title' in body and 'recipe' in body):
        abort(422)

    recipe = body.get('recipe')
    title = body.get('title')

    try:
        drink = Drink(title=title, recipe=json.dumps(recipe))
        drink.insert()
        new_drink = [drink.long()]

        return jsonify({
            'success': True,
            'drinks': new_drink,
        })

    except Exception as e:
        print(f'Error occurred in add_drink(): {e}')
        abort(422)


@app.route("/drinks/<id>", methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(jwt, id):
    """ Update a drink in the database """

    drink = Drink.query.get(id)

    if drink:
        try:

            body = request.get_json()

            title = body.get('title')
            recipe = body.get('recipe')

            if title:
                drink.title = title
            if recipe:
                drink.title = recipe

            drink.update()

            updated_drink = [drink.long()]

            return jsonify({
                'success': True,
                'drinks': updated_drink
            })
        except Exception as e:
            print(f'Error occurred in update_drink(): {e}')
            abort(422)
    else:
        abort(404)


@app.route("/drinks/<id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, id):
    """ Delete a drink from the database """

    drink = Drink.query.get(id)

    if drink:
        try:
            drink.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except Exception as e:
            print(f'Error occurred in delete_drink(): {e}')
            abort(422)
    else:
        abort(404)


@app.errorhandler(422)
def unprocessable(error):
    """ Handle 422 error"""

    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    """ Handle 404 error"""

    return (
        jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }),
        404,
    )


@app.errorhandler(AuthError)
def handle_auth_error(error):
    """ Handle AuthError error"""

    return jsonify({
        "success": False,
        "error": error.status_code,
        'message': error.error
    }), error.status_code
