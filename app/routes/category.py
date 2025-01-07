from flask import jsonify, request, Blueprint
from app.database.models import db,Category
category_bp = Blueprint('category_bp',__name__)

@category_bp.route('/category',methods=['GET','POST'])
def category():
    if request.method == 'GET':
        categories = Category.query.all()
        if not categories:
            return jsonify({'error':'no category found'}),404
        return jsonify({'data':[category.to_json() for category in categories]}),200
    
    if request.method == 'POST':
        data =request.get_json()
        if Category.get_category_by_name(data['name']):
            return jsonify({'error':'category already exists'})

        category = Category(name=data['name'])
        db.session.add(category)
        db.session.commit()
        return jsonify({'data':category.to_json()}),201

@category_bp.route('/category/<string:name>',methods = ['DELETE'])
def delete_category(name):
    category = Category.get_category_by_name(name)
    if not category:
        return jsonify({'error':'category not found'})

    db.session.delete(category)
    db.session.commit()
    return jsonify({'data':'category deleted'}),200

@category_bp.route('/category/<string:name>',methods = ['GET'])
def get_category(name):
    category = Category.get_category_by_name(name)
    if not category:
        return jsonify({'error':'category not found'})
    return jsonify({"data":category.to_json()})

@category_bp.route('/category/<string:name>',methods =['PUT'])
def update_category(name):
    category = Category.get_category_by_name(name)
    if not category:
        return jsonify({'error':'category not found'})
    data = request.get_json()
    if data['name']:
        category.name=data['name']
        db.session.commit()
        return jsonify({'data':'update made'}),200
    else:
        return jsonify({'data':'no update details'}),200
