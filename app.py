import flask
from flask import request, jsonify, render_template, make_response, redirect, url_for
import sqlite3
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime

app = flask.Flask(__name__, template_folder='templates')

app.config['JWT_SECRET_KEY'] = '6384a60d9c326149fc6bbd704f7cd976' # hardcoded in this example, but should be stored in environment variable
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)

# Set default headers
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

@jwt.unauthorized_loader
def unauthorized_loader(callback):
    return redirect(url_for('login_page'))

# Public home page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# Register page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# User home page
@app.route('/user', methods=['GET'])
@jwt_required()
def user():
    return render_template('user.html', username=get_jwt_identity())

# =================================================================================================

# Logout end point
@app.route('/api/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"msg": "Logout successful"}), 200)
    response.set_cookie('access_token_cookie', '', httponly=True, expires=0)
    return response

# Register end point
@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None or password is None:
        return jsonify({"msg": "Username and password are required"}), 400
    
    # Check if user already exists
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({"msg": "User already exists"}), 400
    
    # Add user to database
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return jsonify({"msg": "User created successfully"}), 201


# Login end point
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    # Check if login is correct
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401
    
    access_token = create_access_token(identity=username)
    
    # Set token in HTTP only cookie
    response = make_response(jsonify({"msg": "Login successful"}), 200)
    expires = datetime.datetime.now() + datetime.timedelta(days=1)
    response.set_cookie('access_token_cookie', access_token, httponly=True, expires=expires)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)