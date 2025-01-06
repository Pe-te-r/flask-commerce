from flask import jsonify, request, Blueprint

category_bp = Blueprint('category_bp',__name__)

@category_bp.route('/category',methods=['GET','POST'])
def category():
    if request.method == 'GET':
        return jsonify({'data':'all categories'}),200
    
    if request.method == 'POST':
        return jsonify({'data':'add category'}),201

@category_bp.route('/category/<string:id>',methods = ['DELETE'])
def delete_category(id):
    return jsonify({'data':'category deleted'}),200

@category_bp.route('/category/<string:id>',methods = ['GET'])
def get_category(id):
    return jsonify({"data":f"category details here id={id}"})

@category_bp.route('/category/<string:id>',methods =['PUT'])
def update_category(id):
    return jsonify({'data':'update made'}),200