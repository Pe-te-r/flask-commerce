from flask import Blueprint

orders_bp = Blueprint('orders_bp',__name__)

@orders_bp.route('/orders',methods=['GET'])
def all_orders():
    pass