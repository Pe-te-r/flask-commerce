from flask import  request, jsonify, Blueprint
from flask_jwt_extended import jwt_required,get_jwt
from uuid import UUID,uuid4
from app.database.models import Order,db

orders_bp = Blueprint('orders_bp',__name__)

# get all orders
@orders_bp.route('/orders',methods=['GET'])
@jwt_required()
def all_orders():
    orders = Order.query.all()

    if not orders:
        return jsonify({'error':'orders not found'})
    
    return jsonify({'data':[order.to_json() for order in orders]})

# create order
@orders_bp.route('/orders',methods=["POST"])
@jwt_required()
def add_order():
    data = request.get_json()
    if 'user_id' not in data or 'product_id' not in data:
        return jsonify({'error':'missing infomation'})

    user_id = None
    try:
        user_id = UUID(data['user_id'])
    except Exception:
        return jsonify({'error':'wrong id'})

    new_order = Order(product_id=UUID(data["product_id"]), user_id=user_id, id=uuid4())
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'data':data})


# get one order
@orders_bp.route('/orders/<string:id>',methods=['GET'])
@jwt_required()
def get_one_order(id):

    orders_id = None
    try:
        orders_id = UUID(id)
    except Exception:
        return jsonify({'error':'wrong id'})
    
    order= Order.get_by_id(orders_id)

    if not order:
        return jsonify({'error':'order not found'})

    claims = get_jwt()
    if claims.get("role") != "admin" and order.user_id != claims.get('id'):
        return jsonify({"error": "action not authorized"})
    
    return jsonify({"data": order.to_json()})