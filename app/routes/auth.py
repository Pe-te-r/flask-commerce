from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required,get_jwt_identity
from uuid import UUID
from app.database.models import Auth
from app.database.models import User
from app.helper import  get_otp,get_random_code,send_email

auth_route = Blueprint('auth_route',__name__)

@auth_route.route('/code/:id',methods=['GET'])
@jwt_required()
def get_code(id):    
    user = User.get_by_id(UUID(id))
    if not user:
        return jsonify({'error':'user not found'})

    auth = Auth.get_by_userId(UUID(id))
    if not auth:
        return jsonify({'data':'auth not found'})

    email = get_jwt_identity()
    if user.email != email:
        return jsonify({'error':'action prohibited'})
    send_email(email,auth.random_code)
    return jsonify({'data':f'code :{auth.random_code} sent to email: {email}'})
    


@auth_route.route('/all/:id',methods=['GET'])
@jwt_required()
def sent_auth(id):
    user = User.get_by_id(UUID(id))
    if not user:
        return jsonify({'error':'user not available'})

    if Auth.set_initials(user_id=id,random_code=get_random_code(),totp_secret=get_otp()):
        return jsonify({'data':'code set'})
    
    return jsonify({'error':'code not set'})