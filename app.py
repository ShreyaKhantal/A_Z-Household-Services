from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from app1 import app1
from models import db, Admin
import os
from flask_migrate import Migrate

migrate = Migrate(app1, db)


app = Flask(__name__)
app.secret_key = "ShreyaKhantal:)"

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

upload_folder = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app.config['UPLOAD'] = upload_folder

db.init_app(app)
app.register_blueprint(app1)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # email = 'shreyakhantal@gmail.com'
        # passw = '789'
        # new = Admin(email = email, password=passw)
        # db.session.add(new)
        # db.session.commit()
    app.run(debug=True)
