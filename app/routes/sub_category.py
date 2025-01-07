from flask import  jsonify, request, Blueprint
from uuid import uuid4
from app.database.models import SubCategory,db,Category

sub_category_route  = Blueprint('sub_category_route',__name__)

@sub_category_route.route('/subcategory',methods=['GET','POST'])
def sub_category():
    if request.method =="GET":
        subcategorys = SubCategory.query.all()
        if not subcategorys:
            return jsonify({'error':'no sub category available'})
        
        return jsonify({'data':[subcategory.to_json() for subcategory in subcategorys]})
    
    if request.method == 'POST':
        data  = request.get_json()
        if not data['category'] or not data['name']:
            return jsonify({'error':'missing important info'})
        
        category = Category.get_category_by_name(data["category"])
        subcategory = SubCategory(id=uuid4(),category_id=category.id,name=data['name'])
        db.session.add(subcategory)
        db.session.commit()

        return jsonify({'data':subcategory.to_json()})
