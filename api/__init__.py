from flask import Flask, Blueprint
from api.payagent import payagent_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

default = Blueprint('default', __name__)

@default.route('/api/v1', methods=["GET"])
def index():
    return "Payagent is online"

app.register_blueprint(default)
app.register_blueprint(payagent_blueprint)

if __name__ == "__main__":
    
    app.run(debug=True)