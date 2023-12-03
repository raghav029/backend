from flask import Blueprint, jsonify, request, g, session
from flask_bcrypt import Bcrypt
from db.database import db
from models import User, user_schema
from pyotp import TOTP
import smtplib
from email.mime.text import MIMEText

user = Blueprint("user", __name__)
bcrypt = Bcrypt()

@user.before_request
def before_request():
    g.bcrypt = bcrypt
    
@user.route('/@me')
def get_current_user():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify("Unauthorised asscess"), 401
    user = User.query.filter_by(id=user_id).first()

    return user_schema.jsonify(user)

@user.route('/register', methods=['POST'])
def register_new_user():
    bcrypt = g.bcrypt
    username = request.json['username']
    usn = request.json['usn']
    email = request.json['email']
    ph_number = request.json['ph_number']
    password = request.json['password']
    admin_role = request.json['admin_role']

    user_exist = User.query.filter_by(email=email).first() is not None
    if user_exist:
        return jsonify("User Exist"), 401
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(usn=usn, email=email, password=hashed_password, ph_number=ph_number, username=username, admin_role=admin_role)
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = new_user.id
    return user_schema.jsonify(new_user), 200

@user.route('/login', methods=['POST'])
def login_user():
    bcrypt = g.bcrypt
    # email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    user =  User.query.filter_by(username=username).first()
    
    if user is None:
        return jsonify("Unauthorised access"), 401
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify("Wrong password"), 402
    
    session["user_id"] = user.id
    return user_schema.jsonify(user), 200

@user.route('/logout', methods=['POST'])
def logout_user():
    if 'user_id' in session:
        session.pop('user_id')
    return '200'

# forgot password
# account_sid= 'ACaeff6eb71e88a9c078545a37f177876a'
# auth_token =  '7d54d6e5f9ecf5f35640585de7501e8e'

# create a twilio client
# client = Client(account_sid, auth_token)

# use the client to send msg
# message = client.messages.create(
#    body='Hello, this is your OTP.',
#     from_='rodrigo',  # Your Twilio phone number
#     to='+917803024843'  # Recipient's phone number
# )

# import requests
# resp = requests.post('https://textbelt.com/text', {
#   'phone': '+917803024843',
#   'message': 'Hello world',
#   'key': 'textbelt',
# })
# print(resp.json())