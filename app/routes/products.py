from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required,get_jwt
from uuid import UUID, uuid4
from app.database.models import db,Product,SubCategory

products_bp = Blueprint('products_bp',__name__)

# get all products
@products_bp.route('/products',methods=['GET'])
def all_products():
    products = Product.query.all()
    if not products:
        return jsonify({'error':'no products found'})
    
    return jsonify({'data':[product.to_json() for product in products]})

# add new product
@products_bp.route('/products',methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    if 'name' not in data  or 'price' not in data or 'subcategory' not in data:
        return jsonify({"error":'some information missing'})
    
    subcategory = SubCategory.get_sub_category_by_name(data['subcategory'])
    if not subcategory:
        return jsonify({'error':"category does not exits"})
    
    new_product = Product(name=data['name'],price=data['price'],sub_category_id=subcategory.id,id=uuid4())
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({'data':new_product.to_json()})

# get one product
@products_bp.route('/products/<string:id>',methods = ['GET'])
def one_product(id):
    product = Product.product_by_id(UUID(id))
    if not product:
        return jsonify({'error':'product not found'})
    
    return jsonify({'data':product.to_json()})

# update product
@products_bp.route('/products',methods=['PUT'])
@jwt_required()
def update_product():
    # params
    id = request.args.get('id')
    # auth
    claims = get_jwt()

    product = Product.product_by_id(UUID(id))
    if not product:
        return jsonify({'error':'product not found'})
    
    if product.product_owner != claims.get('id'):
        return jsonify({'error':'action not authorized'})
    

    data = request.get_json()
    if 'name' in data:
        product.name=data['name']
    
    if 'price' in data:
        product.price = data['price']
    
    if 'subcategory_id' in data:
        sub_category = SubCategory.get_sub_category_by_id(UUID(data['subcategory_id']))
        if not sub_category:
            return jsonify({'error':'sub_category not found'})
        
        product.sub_category_id= sub_category.id
    
    db.session.commit()

    return jsonify({'data':'product update successfully'})

# delete product
@products_bp.route('/products',methods=['DELETE'])
@jwt_required()
def delete_product():
    id= request.args.get('id')
    product = Product.product_by_id(UUID(id))
    if not product:
        return jsonify({'error':'product not found'})
    
    claims = get_jwt()
    if product.product_owner !=claims.get('id') and claims.get('role') != 'admin':
        return jsonify({'error':'action not authorized'})

    db.session.delete(product)
    db.session.commit()

    return jsonify({'data':'product deleted successfully'})


