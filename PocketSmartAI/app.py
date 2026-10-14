from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from auth import init_session
from routes.planner_routes import planner_bp
from routes.health_routes import health_bp

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    init_session(app)
    app.register_blueprint(planner_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.errorhandler(404)
    def not_found(error):
        return {"success": False, "error": "Resource not found"}, 404

    @app.errorhandler(413)
    def too_large(error):
        return {"success": False, "error": "Uploaded file is too large"}, 413

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
