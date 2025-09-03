from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS for frontend compatibility

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend to communicate with backend

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"  # Change if using MySQL/PostgreSQL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

# Create database tables
with app.app_context():
    db.create_all()

# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "balance": u.balance} for u in users])

# Add User
@app.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.json
        if "name" not in data or "balance" not in data:
            return jsonify({"error": "Missing 'name' or 'balance'"}), 400

        new_user = User(name=data["name"], balance=data["balance"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added!", "id": new_user.id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Deposit Money
@app.route("/deposit", methods=["POST"])
def deposit():
    try:
        data = request.json
        user = User.query.get(data["id"])
        if not user:
            return jsonify({"message": "User not found"}), 404

        user.balance += data["amount"]
        db.session.commit()
        return jsonify({"message": "Deposit successful!", "balance": user.balance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Withdraw Money
@app.route("/withdraw", methods=["POST"])
def withdraw():
    try:
        data = request.json
        user = User.query.get(data["id"])
        if not user:
            return jsonify({"message": "User not found"}), 404

        if user.balance < data["amount"]:
            return jsonify({"message": "Insufficient balance"}), 400

        user.balance -= data["amount"]
        db.session.commit()
        return jsonify({"message": "Withdrawal successful!", "balance": user.balance})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
