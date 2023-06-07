from flask import Flask
from userAuthentication.models import db
from userAuthentication.loginMgr import login_manager
from userAuthentication.user_blueprint import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "arunisto"
login_manager.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(user_bp)
if __name__ == "__main__":
    app.run(debug=True)
