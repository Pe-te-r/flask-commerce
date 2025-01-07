from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from uuid import uuid4
from app.database.models import db,Category
category_bp = Blueprint('category_bp',__name__)

# get all category and add category
@category_bp.route('/category',methods=['GET','POST'])
def category():
    if request.method == 'GET':
    
        categories = Category.query.all()
        if not categories:
            return jsonify({'error':'no category found'}),404
        return jsonify(
            {"data": [category.to_json(sub_category=True) for category in categories]}
        ), 200
    
    if request.method == 'POST':
        data =request.get_json()
        if Category.get_category_by_name(data['name']):
            return jsonify({'error':'category already exists'})

        category = Category(name=data['name'],id=uuid4())
        db.session.add(category)
        db.session.commit()
        return jsonify({"data": category.to_json()}), 201

# delete category
@category_bp.route('/category/<string:name>',methods = ['DELETE'])
@jwt_required()
def delete_category(name):
    category = Category.get_category_by_name(name)
    if not category:
        return jsonify({'error':'category not found'})

    db.session.delete(category)
    db.session.commit()
    return jsonify({'data':'category deleted'}),200

# get one category
@category_bp.route('/category/<string:name>',methods = ['GET'])
def get_category(name):
    category = Category.get_category_by_name(name)
    if not category:
        return jsonify({'error':'category not found'})
    return jsonify({"data":category.to_json()})

# update one category
@category_bp.route('/category/<string:name>',methods =['PUT'])
@jwt_required()
def update_category(name):
    print(name)
    category = Category.get_category_by_name(name)
    print(category)
    if not category:
        return jsonify({'error':'category not found'})
    data = request.get_json()
    if data['name']:
        category.name=data['name']
        db.session.commit()
        return jsonify({'data':'update made'}),200
    else:
        return jsonify({'data':'no update details'}),200
