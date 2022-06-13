import os

from flask import Flask
from data.models import db
from api.api import app as api
from werkzeug.exceptions import HTTPException

from api.handlers import handle_http_exception, handle_exception

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', None)

with app.app_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()

app.register_blueprint(api)
app.register_error_handler(HTTPException, handle_http_exception)
app.register_error_handler(500, handle_exception)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

