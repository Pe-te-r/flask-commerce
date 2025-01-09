from flask import jsonify, Blueprint
from uuid import UUID
from app.database.models import Auth
from app.helper import  get_otp,get_random_code

auth_route = Blueprint('auth_route',__name__)

@auth_route.route('/code/:id',methods=['GET'])
def get_code(id):
    auth = Auth.get_by_userId(UUID(id))


@auth_route.route('/auth/:id',methods=['GET'])
def sent_auth(id):
    if Auth.set_initials(user_id=id,random_code=get_random_code(),totp_secret=get_otp()):
        return jsonify({'data':'code set'})
    
    return jsonify({'error':'code not set'})