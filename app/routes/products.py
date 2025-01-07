from flask import request, jsonify, Blueprint
from uuid import uuid4
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
@products_bp.route('/products/<string:name>',methods = ['GET'])
def one_product(name):
    product = Product.product_by_name(name)
    if not product:
        return jsonify({'error':'product not found'})
    
    return jsonify({'data':product.to_json()})

# update product
@products_bp.route('/products/<string:name>',methods=['PUT'])
def update_product(name):
    product = Product.product_by_name(name)
    if not product:
        return jsonify({'error':'product not found'})

    data = request.get_json()
    if 'name' in data:
        product.name=data['name']
    
    if 'price' in data:
        product.price = data['price']
    
    if 'subcategory' in data:
        sub_category = SubCategory.get_sub_category_by_name(name)
        if not sub_category:
            return jsonify({'error':'sub_category not found'})
        
        product.sub_category_id= sub_category.id
    
    db.session.commit()

    return jsonify({'data':'product update successfully'})

# delete product
@products_bp.route('/products/<string:name>',methods=['DELETE'])
def delete_product(name):
    product = Product.product_by_name(name)
    if not product:
        return jsonify({'error':'product not found'})
    
    db.session.delete(product)
    db.session.commit()

    return jsonify({'data':'product deleted successfully'})


