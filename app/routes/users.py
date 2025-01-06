from flask import request, jsonify, Blueprint
from app.database.models import User,db

user_bp =Blueprint('user_bp',__name__)

@user_bp.route('/users',methods=['GET'])
def get_users():
    users= User.query.all()
    return jsonify({'data':[user.to_json() for user in users]})

@user_bp.route('/users',methods=['POST'])
def register_user():
    data = request.get_json()

    if 'email' not in data or  'password' not  in data or 'last_name' not in data or 'first_name' not in data:
        return jsonify({'error':'some information missing'})
    
    if User.get_by_email(data['email']):
        return jsonify({'error':'email already exists'}),409

    password = data['password']
    del data['password']

    new_user = User(first_name=data['first_name'],last_name=data['last_name'],email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    new_user.save_password(password)
    return jsonify({'data':data}),201

@user_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    user = User.get_by_email(email=data['email'])
    if not user:
        return jsonify({'error':'Email not found'}),404
    if user.verify_password(data["password"]):
        return jsonify({'data':user.to_json()}),200
        
    return jsonify({'error':'an error'}),

@user_bp.route('/users',methods=['DELETE'])
def delete_user():
    data = request.get_json()
    user = User.get_by_email(data['email'])
    return user