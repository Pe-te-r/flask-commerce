
def register_routes(app):
    from app.routes.users import user_bp
    app.register_blueprint(user_bp,url_prefix='/api')
