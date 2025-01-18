from flask import  request,  jsonify, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from uuid import UUID
from app.database.models import Auth,db
from app.database.models import User
# from app.helper import  get_random_code,send_email,verify_otp,verify_random_code
from app.helper.totp import get_otp
from app.helper.totp import verify_otp
from app.helper.random_code import get_random_code
from app.helper.random_code import verify_random_code

auth_route = Blueprint('auth_route',__name__)

# set all
@auth_route.route('/auth',methods=['POST'])
@jwt_required()
def sent_auth():
    data = request.get_json()
    id = None
    if 'id' not in data:
        return jsonify({'error':'user id missing'})
    try:
        id = UUID(data['id'])
    except Exception:
        return jsonify({'error':'wrong id'})
    user = User.get_by_id(id)
    if not user:
        return jsonify({'error':'user not available'})
    email = get_jwt_identity()
    if user.email != email:
        return jsonify({'error':'action not permited'})
    
    auth= Auth.get_by_userId(id)
    if  auth is not None:
        return jsonify({'error':'auth already available'})

    if Auth.set_initials(user_id=id,random_code=get_random_code(),totp_secret=get_otp()):
        return jsonify({'data':'code set'})
    
    return jsonify({'error':'code not set'})

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
    # send_email(email,auth.random_code)
    return jsonify({'data':f'code :{auth.random_code} sent to email: {email}'})
    
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
        return jsonify({'error':'you are not authorized'})
    
    data = request.get_json()

    if 'code' not in data:
        return jsonify({'error':'code not provided'})
    
    code = data['code']
    if  verify_otp(auth.totp_secret,str(code)):
        return jsonify({'data':True})
    else:
        return jsonify({'data':False})
        



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

