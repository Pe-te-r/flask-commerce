from flask import  request, jsonify, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from flask_jwt_extended import create_access_token,get_jwt
from uuid import uuid4,UUID
from app.database.models import User,db,Role_Enum
from app.helper.mails import send_email
user_bp =Blueprint('user_bp',__name__)

# get one user
@user_bp.route("/users/<string:id>", methods=["GET"])
@jwt_required()
def get_user(id):
    print(id)
    user = User.get_by_id(UUID(id))
    if not user:
        return jsonify({"error": "user not found"}), 409

    return jsonify(user.to_json())

# get all users
@user_bp.route('/users',methods=['GET'])
@jwt_required()
def get_users():
    # params
    orders = request.args.get('orders')

    claims = get_jwt()
    role = claims.get('role')
    if role !='admin':
        return jsonify({'error':'user not allowed'}),403

    users= User.query.all()
    if not users:
        return jsonify({"error": "no user  found"}), 404
    return jsonify({'data':[user.to_json(show_orders=orders) for user in users]})

# register users
@user_bp.route('/users',methods=['POST'])
def register_user():
    try:
        data = request.get_json()

        if 'email' not in data or  'password' not  in data or 'last_name' not in data or 'first_name' not in data :
            return jsonify({'error':'some information missing'})
        
        if User.get_by_email(data['email']):
            return jsonify({'error':'email already exists'}),409
        
        password = data['password']
        del data['password']

        role_enum=None
        if 'role' in data:
            role_enum= Role_Enum(data['role']) 

        new_user = User(first_name=data['first_name'],last_name=data['last_name'],email=data['email'],id = uuid4(),role=role_enum)
        db.session.add(new_user)
        db.session.commit()
        # db.session.refresh(new_user)
        new_user.save_password(password)
        print('here before all')
        # user = {'first_name':new_user.first_name}
        print('here before all2')
        # send_email(
        #     subject="Welcome to Phantom Market!",
        #     recipients=new_user.email,
        #     template_name="register",
        #     user=user,
        # )
        send_email(firstname=new_user.first_name,email=new_user.email)
        print('mail.sent')
        return jsonify({'data':'success'}),201
    except Exception  as e:
        print(e)
        return jsonify('error')


#login user
@user_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    user = User.get_by_email(email=data['email'])

    if not user:
        return jsonify({'error':'Email not found'}),404
    if user.verify_password(data["password"]):
        more_info ={'role':user.role.value,'id':user.id}
        token= create_access_token(identity=user.email,additional_claims=more_info)
        return jsonify({"data":{ "user":user.to_json(), "token":token} }),200
    else:
        return jsonify({'error':'password not correct'}),401
        
    return jsonify({'error':'an error'}),400

# delete user
@user_bp.route('/users',methods=['DELETE'])
@jwt_required()
def delete_user():
    data = request.get_json()
    user = User.get_by_email(data['email'])
    if not user:
        return jsonify({'error':'user does not exists'}),409
    # auth
    token_mail=get_jwt_identity()
    claims = get_jwt()
    if token_mail != user.email and claims.get('role') != 'admin':
        return jsonify({'error':'cannot delete another user'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'data':'user delete'}),200

# update user
@user_bp.route('/users',methods=['PUT'])
@jwt_required()
def update_user():
    # params
    email = request.args.get('email')
    id = request.args.get('id')
    # auth
    token_mail = get_jwt_identity()
    claims = get_jwt()

    user=None
    if email:
        user = User.get_by_email(email=email)
    
    if id:
        user = User.get_by_id(id=id)
    if not user:
        return jsonify({'error':'user not found'})
    
    if user.email != token_mail and claims.get('role') != 'admin':
        return jsonify({'error':'cannot updated another person data'})
    data = request.get_json()

    if 'email'  in data:
        user.email = data['email']
    if 'last_name' in data:
        user.last_name=data['last_name']
    if 'first_name' in data:
        user.first_name=data['first_name']
    if 'role' in data:
        user.role = Role_Enum(data['role'])
    db.session.commit()

    return jsonify({'data':user.to_json()})