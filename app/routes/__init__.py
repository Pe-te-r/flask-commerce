
def register_routes(app):
    from app.routes.users import user_bp
    from app.routes.category import category_bp
    from app.routes.sub_category import sub_category_route
    from app.routes.products import products_bp

    app.register_blueprint(user_bp,url_prefix='/api')
    app.register_blueprint(category_bp,url_prefix='/api')
    app.register_blueprint(sub_category_route, url_prefix="/api")
    app.register_blueprint(products_bp, url_prefix="/api")
