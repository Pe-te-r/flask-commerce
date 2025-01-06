
def register_routes(app):
    from app.routes.users import user_bp
    from app.routes.category import category_bp
    app.register_blueprint(user_bp,url_prefix='/api')
    app.register_blueprint(category_bp,url_prefix='/api')
