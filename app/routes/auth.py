from flask import   request,  jsonify, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity,get_jwt
from uuid import UUID
from app.database.models import Auth,db
from app.database.models import User,Password
# from app.helper import  get_random_code,send_email,verify_otp,verify_random_code
from app.helper.totp import get_otp
from app.helper.totp import verify_otp
from app.helper.random_code import get_random_code
from app.helper.random_code import verify_random_code
from app.helper.mails import send_email

auth_route = Blueprint('auth_route',__name__)


# # set all
@auth_route.route("/auth", methods=["POST"])
@jwt_required()
def sent_auth():
    data = request.get_json()
    id = None
    if "id" not in data:
        return jsonify({"error": "user id missing"})
    try:
        id = UUID(data["id"])
    except Exception:
        return jsonify({"error": "wrong id"})

    # Use id directly (no need for UUID(id) again)
    user = User.get_by_id(id)
    print(user)
    print('on auth')
    if not user:
        return jsonify({"error": "user not available"})

    email = get_jwt_identity()
    if user.email != email:
        return jsonify({"error": "action not permitted"})

    auth = Auth.get_by_userId(id)
    if auth is not None:
        return jsonify({"error": "auth already available"})

    random_code = get_random_code()
    if Auth.set_initials(user_id=id, random_code=random_code, totp_secret=get_otp()):
        send_email(
            firstname=user.first_name,
            email=user.email,
            template="code",
            data=random_code,
        )
        return jsonify({"data": "code sent"}), 200

    return jsonify({"error": "code not set"})


# "f1910bc2-2e80-4a44-baba-9f749352ce00"
# "f1910bc2-2e80-4a44-baba-9f749352ce00"


# send random code
@auth_route.route('/code/<string:id>',methods=['GET'])
@jwt_required()
def get_code(id):    
    user_id = None
    try:
        user_id = UUID(id)
        if not user_id:
            return jsonify({'error':'id not provided'})
    except Exception :
        return jsonify({'error':'wrong id'})
    user = User.get_by_id(user_id)
    if  user is None:
        return jsonify({'error':'user not found'})

    auth = Auth.get_by_userId(user_id)
    if not auth:
        return jsonify({'data':'auth not found'})

    email = get_jwt_identity()
    if user.email != email:
        return jsonify({'error':'action prohibited'})
    send_email(firstname=user.first_name,email=user.email,template='code',data=auth.random_code)
    return jsonify({'data':'code sent to the email'})
    
# verify random code
@auth_route.route('/code',methods=['POST'])
@jwt_required()
def verify_code():
    data = request.get_json()
    if 'id' not in data:
        return jsonify({'error':'id missing'})
    
    if 'code' not in data:
        return jsonify({'error':'code missing'})
    
    user_id =None
    try:
        user_id = UUID(data["id"])
    except Exception:
        return jsonify({'error':'wrong id'})
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'error':'user not available'})
    
    email = get_jwt_identity()
    if user.email != email:
        return jsonify({'error':'action not authorized'})
    auth = Auth.get_by_userId(user_id)

    if verify_random_code(auth.random_code,data['code']):
        return jsonify({'data':True})
    return jsonify({'data':False})


# update verification code
@auth_route.route('/code',methods=['PUT'])
@jwt_required()
def update_code():
    data = request.get_json()
    if 'id' not in data:
        return jsonify({'error':'id is missing'})
    
    user_id = None
    try:
        user_id = UUID(data['id'])
    except Exception :
        return jsonify({'error':'wrong id'})
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'error':'user not found'})
    
    email = get_jwt_identity()
    
    if user.email != email:
        return jsonify({'error':'An authorized'})

    auth = Auth.get_by_userId(user_id)
    if not auth:
        return jsonify({'error':'code not set'})
    auth.random_code =get_random_code()

    db.session.commit()
    return jsonify({'data':'code updated'})

# verify totp
@auth_route.route('/totp/<string:id>',methods=['POST'])
@jwt_required()
def verify_totp(id):
    user_id = None
    try:
        user_id=UUID(id)
    except Exception:
        return jsonify({'error':'wrong id'})
    auth = Auth.get_by_userId(user_id)
    if not auth:
        return jsonify({'error':'not available'})
    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'error':'user not found'})

    email = get_jwt_identity()
    if user.email != email:
        return jsonify({'error':'you are not authorized'}),403
    
    data = request.get_json()

    if 'code' not in data:
        return jsonify({'error':'code not provided'}),400
    
    code = data['code']
    if  verify_otp(auth.totp_secret,str(code)):
        auth.totp_enabled=True
        db.session.commit()
        return jsonify({'data':True}),200
    else:
        return jsonify({'data':False}),401
        

@auth_route.route('/verify/<string:id>',methods=['POST'])
@jwt_required()
def verify_2fa(id):
    claims=get_jwt()
    if id != claims.get("id"):
        return jsonify({"error": "action not authorize"}), 401
    auth_totp = Auth.get_by_userId(UUID(id))
    if not auth_totp:
        return jsonify({'error':'not setuped'}),404
    data = request.get_json()
    print(data)
    print('here one')
    if 'random_code' in data and not  verify_random_code(auth_totp.random_code,data['random_code']):
        return jsonify({'error':'email code error'}),400
    print('here two')
    
    if 'totp_code' in data and not verify_otp(auth_totp.totp_secret,data['totp_code']):
        return jsonify({'error':'2FA code error'}),400
    print('here three')
    
    return jsonify({'data':True})


# get totp secret code
@auth_route.route('/totp/<string:id>',methods=['GET'])
@jwt_required()
def get_totp(id):
    claims=get_jwt()
    if id != claims.get('id'):
        return jsonify({'error':'action not authorize'}),401
    auth_totp = Auth.get_by_userId(UUID(id))
    if auth_totp.totp_enabled:
        return jsonify(True)
    return jsonify(auth_totp.totp_secret)

# update totp secret code
@auth_route.route('/totp',methods =['PUT'])
@jwt_required()
def update_totp():
    data = request.get_json()
    if 'id' not in data:
        return jsonify({'error':'user id is missing'})
    
    id=None
    try:
        id = UUID(data['id'])
    except Exception :
        return jsonify({'error':'wrong id'})

    user = User.get_by_id(UUID(id))
    if not user:
        return jsonify({'error':'user not found'})
        
    email = get_jwt_identity()
        
    if user.email != email:
        return jsonify({'error':'An authorized'})

    auth = Auth.get_by_userId(UUID(id))
    if not auth:
        return jsonify({'error':'code not set'})
    
    auth.totp_secret=get_otp()
    db.session.commit()

    return jsonify({'data':'totp updated'})

@auth_route.route('/password/<string:id>',methods=['PUT'])
@jwt_required()
def change_pass(id):
    user = User.get_by_id(UUID(id))
    if not user:
        return jsonify({'error':'user not found'}),404
    
    email = get_jwt_identity()
    if email != user.email:
        return jsonify({'error':'not authorize'}),401
    
    password= Password.get_password_by_userid(UUID(id))

    data = request.get_json()
    print(data)
    if 'password' in data:
        password.password = Password.hash_password(data['password'])
        db.session.commit()
        db.session.refresh(password)
        print(password.password)
        return jsonify({'data':'password updated'})
    
    return jsonify({'error':'password not sent'})

