from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required,get_jwt
from uuid import UUID, uuid4
from app.database.models import db,Category
category_bp = Blueprint('category_bp',__name__)

# get all category
@category_bp.route('/category',methods=['GET'])
def all_category():    
    categories = Category.query.all()
    if not categories:
        return jsonify({'error':'no category found'}),404
    sub_category = request.args.get('subcategory')
    return jsonify({"data": [category.to_json(sub_category=sub_category) for category in categories]}), 200
    


# add category
@category_bp.route('/category',methods=['POST'])
@jwt_required()
def category():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "action not authorized"})
    data =request.get_json()
    if Category.get_category_by_name(data['name']):
        return jsonify({'error':'category already exists'})
    category = Category(name=data['name'],id=uuid4())
    db.session.add(category)
    db.session.commit()
    return jsonify({"data": category.to_json()}), 201

# delete category
@category_bp.route('/category/<string:id>',methods = ['DELETE'])
@jwt_required()
def delete_category(id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error':'action not authorized'})

    category_id= None
    try:
        category_id=UUID(id)
    except Exception:
        return jsonify({'error':'wrong id'})
    category = Category.get_category_by_id(category_id)
    if not category:
        return jsonify({'error':'category not found'})

    db.session.delete(category)
    db.session.commit()
    return jsonify({'data':'category deleted'}),200

# get one category
@category_bp.route('/category/<string:id>',methods = ['GET'])
def get_category(id):
    category_id= None
    try:
        category_id=UUID(id)
    except Exception:
        return jsonify({'error':'wrong id'})

    category = Category.get_category_by_id(category_id)
    if not category:
        return jsonify({'error':'category not found'})
    
    sub_category = request.args.get('subcategory')
    return jsonify({"data": category.to_json(sub_category=sub_category)})

# update one category
@category_bp.route('/category/<string:id>',methods =['PUT'])
@jwt_required()
def update_category(id):
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error':'action not authorized'})
    category_id= None
    try:
        category_id=UUID(id)
    except Exception:
        return jsonify({'error':'wrong id'})
    category = Category.get_category_by_id(category_id)
    if not category:
        return jsonify({'error':'category not found'})
    data = request.get_json()
    if data['name']:
        category.name=data['name']
        db.session.commit()
        return jsonify({'data':'update made'}),200
    else:
        return jsonify({'data':'no update details'}),200
