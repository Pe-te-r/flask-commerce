from app.database import db,bcypt
from uuid import uuid4

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.UUID(),primary_key=True,default=uuid4())
    first_name=db.Column(db.String(80),nullable=False)
    last_name=db.Column(db.String(80),nullable=False)
    email=db.Column(db.String(100),nullable=False,unique=True)
    
    # relationship
    password = db.Relationship('Password',back_populates='user',uselist=False,cascade='all, delete')

    def  __repr__(self):
        return f'User({self.first_name} {self.last_name})'
    
    def to_json(self):
        return    {'id':str(self.id),'first_name':self.first_name,'last_name':self.last_name,'email':self.email}

    def save_password(self,password):
        self.password_saving=Password(user_id = self.id,password=Password.hash_password(password))
        db.session.add(self.password_saving)
        db.session.commit()
    
    def verify_password(self,password):
        hashed_pass = Password.query.filter_by(user_id=self.id).first()
        return Password.verify(hashed_pass.password,password)

    
    @classmethod
    def get_by_email(cls,email):
        return cls.query.filter_by(email=email).first()


class Password(db.Model):
    __tablename__='password'
    user_id = db.Column(db.UUID(),db.ForeignKey('user.id'),nullable=False,primary_key=True)
    password= db.Column(db.String(255),nullable=False)

    # relationship
    user = db.Relationship('User',back_populates='password',uselist=False)

    def __repr__(self):
        return f'Password({self.password})'
    
    @staticmethod
    def hash_password(password):
        return bcypt.generate_password_hash(password=password.encode('utf-8'))
        

    @staticmethod
    def verify(hashed_pass,password):
        return bcypt.check_password_hash(hashed_pass,password)
    

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.UUID(),primary_key=True,nullable=False,default=uuid4())
    name  = db.Column(db.String(255),nullable=False,unique=True)

    # relationship
    subcategory = db.Relationship("SubCategory",back_populates='category',uselist=True)

    def to_json(self,sub_category=False):
        if sub_category:
            return{
                'id':self.id,
                'name':self.name,
                'subcategory':{
                    [category.to_json() for category in self.subcategory]
                }
            }

        return{
            'id':self.id,
            'name':self.name
        }
    
    @classmethod
    def get_category_by_name(cls,name):
        return cls.query.filter_by(name=name).first()
    

class SubCategory(db.Model):
    __tablename__ = 'subcategory'
    id=db.Column(db.UUID(),primary_key=True,nullable=False,default=uuid4())
    category_id = db.Column(db.UUID(),db.ForeignKey('category.id'),nullable=False)
    name = db.Column(db.String(100),unique=True,nullable=False)

    # relationship
    category = db.Relationship('Category',back_populates='subcategory',uselist=False)

    def to_json(self):
        return{
            'id':self.id,
            'category_id':self.category_id,
            'name':self.name
        }