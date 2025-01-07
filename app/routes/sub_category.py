from flask import  jsonify, request, Blueprint
from uuid import uuid4
from app.database.models import SubCategory,db,Category

sub_category_route  = Blueprint('sub_category_route',__name__)

# create sub_category and get all sub_category
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
        if not category:
            return jsonify({'error':'category not available'})
        sub_category_exits=SubCategory.get_sub_category_by_name(data['name'])
        if sub_category_exits:
            return jsonify({'error':'sub category already available'})
        subcategory = SubCategory(id=uuid4(),category_id=category.id,name=data['name'])
        db.session.add(subcategory)
        db.session.commit()

        return jsonify({'data':subcategory.to_json()})

# update sub_category
@sub_category_route.route('/subcategory/<string:subcategory>',methods = ['PUT'])
def update_sub_category(subcategory):
    print('update')
    sub_category = SubCategory.get_sub_category_by_name(subcategory)

    if not sub_category:
        return jsonify({'error':'subcategory not found'})

    data = request.get_json()
    if 'name' in data:
        sub_category.name = data['name']
    
    if 'category' in data:
        category = Category.get_category_by_name(data['category'])
        if not category:
            return jsonify({'error':'category does not exists'})
        
        print(category.id)
        print(sub_category.category_id)
        if category.id != sub_category.category_id:
            sub_category.category_id=category.id

    db.session.commit()

    return jsonify({'data':'subcategory updated'})

# delete sub_category
@sub_category_route.route('/subcategory/<string:subcategory>',methods = ['DELETE'])
def delete_sub_category(subcategory):
    print('delete')
    sub_category = SubCategory.get_sub_category_by_name(subcategory)
    if not sub_category:
        return jsonify({'error':'sub category does not exits'}),404
    
    db.session.delete(sub_category)
    db.session.commit()
    return jsonify({'data':'sub category deleted successfully'})

# get one sub_category
@sub_category_route.route('/subcategory/<string:subcategory>',methods =['GET'])
def get_one_sub_category(subcategory):
    print(subcategory)
    sub_category = SubCategory.get_sub_category_by_name(subcategory)
    if not sub_category:
        return jsonify({'error':'sub category does not exists'})
    
    return jsonify({'data':sub_category.to_json()})
