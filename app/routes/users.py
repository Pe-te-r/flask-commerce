from flask import  request, jsonify, Blueprint
from app.database.models import User,db

user_bp =Blueprint('user_bp',__name__)

# get one user
@user_bp.route("/users/<string:email>", methods=["GET"])
def get_user(email):
    user = User.get_by_email(email)
    if not user:
        return jsonify({"error": "user not found"}), 409

    return jsonify(user.to_json())

# get all users
@user_bp.route('/users',methods=['GET'])
def get_users():
    users= User.query.all()
    if not users:
        return jsonify({"error": "no user  found"}), 409

    return jsonify({'data':[user.to_json() for user in users]})

# register users
@user_bp.route('/users',methods=['POST'])
def register_user():
    data = request.get_json()

    if 'email' not in data or  'password' not  in data or 'last_name' not in data or 'first_name' not in data:
        return jsonify({'error':'some information missing'})
    
    if User.get_by_email(data['email']):
        return jsonify({'error':'email already exists'}),409

    new_user = User(first_name=data['first_name'],last_name=data['last_name'],email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    new_user.save_password(data['password'])
    return jsonify({'data':data}),201

#login user
@user_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    user = User.get_by_email(email=data['email'])
    if not user:
        return jsonify({'error':'Email not found'}),404
    if user.verify_password(data["password"]):
        return jsonify({'data':user.to_json()}),200
        
    return jsonify({'error':'an error'}),

# delete user
@user_bp.route('/users',methods=['DELETE'])
def delete_user():
    data = request.get_json()
    user = User.get_by_email(data['email'])
    if not user:
        return jsonify({'error':'user does not exists'}),409
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'data':'user delete'}),200

# update user
@user_bp.route('/users/<string:email>',methods=['PUT'])
def update_user(email):
    user = User.get_by_email(email=email)
    if not user:
        return jsonify({'error':'user not found'})
    
    print(user.password.password)
    data = request.get_json()

    if data['email']:
        user.email = data['email']
    if data['last_name']:
        user.last_name=data['last_name']
    if data['first_name']:
        user.first_name=data['first_name']
    
    db.session.commit()

    return jsonify(data)