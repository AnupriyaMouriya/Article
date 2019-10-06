from flask import Flask, request, jsonify
from werkzeug.exceptions import *
from flask_jsonschema_validator import JSONSchemaValidator
from model import *
import re
import jsonschema
from flask import Response


app = Flask(__name__)
JSONSchemaValidator( app = app, root = "schemas" )

@app.errorhandler(Exception)
def handle_error(error):
    code = 500
    if isinstance(error, HTTPException):
        code = error.code
    return jsonify(error=str(error)),code


@app.errorhandler( jsonschema.ValidationError )
def onValidationError( e ):
  return Response( "Validation Error: " + str( e ), 400 )


def is_valid_id(id):
    return re.fullmatch("[0-9]+",id)


@app.route('/article/<user_id>/subscribe/<article_id>',methods=['POST'])
def user_subscribes_article(user_id,article_id):
    if not is_valid_id(user_id):
        raise BadRequest("Invalid user id")
    if not is_valid_id(article_id):
        raise BadRequest("Invalid article id")
    user=People.query.filter_by(user_id=user_id).first()
    if not user:
        raise NotFound("user not found")
    article = Article.query.filter_by(article_id=article_id).first()
    if not article:
        raise NotFound("Article not present")
    for traverse_each_article in user.subsriptions:
        if article.article_id== traverse_each_article.article_id:
            return jsonify("Article already subscribed"),200
    article.subscibers.append(user)
    db.session.commit()
    return jsonify({"user_id": user.user_id, "article_id": article.article_id}), 200


@app.route('/user/add',methods=['POST'])
@app.validate('users', 'register' )
def add_user():
    user = request.json
    name = request.json['name']
    email=request.json['email']
    if  People.query.filter_by(user_email=email).first() :
        raise BadRequest("email already exist ")
    user_add=People(name=name,email=email)
    db.session.add(user_add)
    db.session.commit()
    return jsonify(user),201


@app.route('/user', methods=['GET'])
def all_user():
    list = []
    for user in People.query.all():
        list.append({"user_id": user.user_id, "user_name": user.user_name,"user_email":user.user_email})
    return jsonify(list), 200


@app.route('/article', methods=['GET'])
def all_article():
        list = []
        for article in Article.query.all():
            list.append({"article_id": article.article_id, "topic": article.topic, "content": article.content})
        return jsonify(list), 200



@app.route('/article/<user_id>', methods=['GET'])
def articles_of_user(user_id):
    list = []
    if not is_valid_id(user_id):
        raise BadRequest("Invalid user id")
    user=People.query.filter_by(user_id=user_id).first()
    if not user:
        raise BadRequest("user not found")
    for article in user.subsriptions:
        list.append({"article_id": article.article_id})
    return jsonify(list), 200


@app.route('/<wrong_api>',methods=['GET','POST','PUT','DELETE'])
def other(wrong_api):
    print("wrong API")
    raise NotFound("The request URL is not found on server")


if __name__ == '__main__':
    app.run(debug=True , host="0.0.0.0")
