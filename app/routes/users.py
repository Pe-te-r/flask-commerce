from flask import request, jsonify, Blueprint
from app.database.models import User,db,Password

user_bp =Blueprint('user_bp',__name__)

@user_bp.route('/users',methods=['GET'])
def get_users():
    # user = User(first_name='peter',last_name='wahu',email='phantom8526@duck.go')
    # print(user)
    # db.session.add(user)
    # db.session.commit()
    print('here 1')
    users= User.query.all()
    print('here 2')
    print(users)
    return jsonify({'data':[user.to_json() for user in users]})

@user_bp.route('/users',methods=['POST'])
def register_user():
    data = request.get_json()

    if 'email' not in data or  'password' not  in data or 'last_name' not in data or 'first_name' not in data:
        return jsonify({'error':'some information missing'})
    password = data['password']
    del data['password']

    new_user = User(first_name=data['first_name'],last_name=data['last_name'],email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    new_user.save_password(password)
    return jsonify({'data':data})

@user_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    # user = User.query.filter_by(email=data['email']).first
    user = User.get_by_email(email=data['email'])
    if not user:
        return jsonify({'error':'Email not found'})
    # password = Password.query.filter_by(user_id=user.id)
    if user.verify_password(data["password"]):

        return jsonify({'data':user.to_json()})
    return jsonify({'error':'an error'})