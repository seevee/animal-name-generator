from flask import Blueprint, jsonify, request, session
from sqlalchemy_db_instance import db
from models import User

users_api = Blueprint('users_api', __name__)

@users_api.route('/duplicate-user-test', methods=["POST"])
def test_duplicate_user():
    username = request.json["username"]
    user_in_db = db.session.query(User).filter(User.username == username).all()
    user_in_db_results = [{"id": user.id, "user_username": user.username} for user in user_in_db]
    return jsonify({"does_the_user_exist": user_in_db_results})

@users_api.route('/add-user', methods=["POST"])
def add_user():
    new_user = User()
    new_user.username = request.json["username"]
    new_user.password = request.json["password"]
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"username": new_user.username, "password": new_user.password})

@users_api.route('/login', methods=["POST"])
def login():
    username = request.json['username']
    password = request.json['password']
    users = User.query.filter_by(username=username)
    if users.count() == 1:
        user = users.first()
        if password == user.password:
            session['user'] = user.username
            return jsonify({"username": user.username})
    return jsonify(success = False)

@users_api.route('/users', methods=['POST', 'GET'])
def test_users_in_session():
    if 'user' in session:
        return jsonify({"userInSession": session['user']})
    return jsonify(success=False)

@users_api.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['user']
    return jsonify(success=True)