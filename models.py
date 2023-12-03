from db.database import db
from flask_marshmallow import Marshmallow
from uuid import uuid4
import secrets

# unique id generation
def get_uuid():
    return uuid4().hex
# unique id for otp
def get_otp_secret_key():
    return secrets.token_hex(20)

ma = Marshmallow()

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    admin_role = db.Column(db.Boolean, default=True)
    user_name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20))
    dept = db.Column(db.String(30))

    def __init__(self, admin_role, user_name, password, role, dept):
        self.admin_role = admin_role
        self.user_name = user_name
        self.password = password
        self.role = role
        self.dept = dept

class AdminSchema(ma.Schema):
    class Meta:
        fields = ('id', 'admin_role', 'user_name', 'password', 'role', 'dept')

admin_schema = AdminSchema()
admin_schema = AdminSchema(many=True)

class ClubEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_uri = db.Column(db.String(50), nullable=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.String(30), nullable=False)
    club = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer)
    venue = db.Column(db.String(50))
    date = db.Column(db.String(30))
    time = db.Column(db.String(25))
    user_club_events = db.relationship('User', secondary='user_club_events', backref='club_events', lazy=True)

    def __init__(self, title, description, club, event_type, amount, venue, date, time, image_uri):
        self.image_uri = image_uri
        self.title = title
        self.description = description
        self.club = club
        self.event_type = event_type
        self.amount = amount
        self.venue = venue
        self.date = date
        self.time = time

class ClubEventsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'event_type', 'amount', 'venue', "date", 'time')

club_event_schema = ClubEventsSchema()
club_events_schema = ClubEventsSchema(many=True)

# event model
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_uri = db.Column(db.String(300))
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    event_type = db.Column(db.String(10))
    dept = db.Column(db.String(20))
    amount = db.Column(db.Integer)
    venue = db.Column(db.String(50))
    event_mode = db.Column(db.String(12))
    date = db.Column(db.String(30))
    time = db.Column(db.String(25))
    expiration = db.Column(db.Boolean, default=False)
    user_events = db.relationship('User', secondary='user_event', backref='events', lazy=True)
    event_attendece = db.relationship('User', secondary='event_attendence', backref='attended_events', lazy=True)



    def __init__(self, image_uri, title, description, event_type, dept, amount, venue, date, time, event_mode, expiration):
        self.image_uri = image_uri
        self.title = title
        self.description = description
        self.event_type = event_type
        self.venue = venue
        self.date = date
        self.time = time
        self.event_mode = event_mode
        self.expiration = expiration
        self.dept = dept
        self.amount = amount

class EventSchema(ma.Schema):
    class Meta:
        fields = ('id', 'image_uri', 'title', 'description', 'event_type', 'venue', "date", 'time', 'event_mode', 'expiration', 'amount', 'dept')

event_schema = EventSchema()
events_schema = EventSchema(many=True)

class EventNameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title')

eventName_schema = EventNameSchema()
eventsName_schema = EventNameSchema(many=True)

class UserClubEvents(db.Model):
    __tablename__ = "user_club_events"
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), primary_key=True)
    club_event_id = db.Column(db.Integer, db.ForeignKey('club_events.id'), primary_key=True)
    applied = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, club_event_id, applied):
        self.user_id = user_id
        self.club_event_id = club_event_id
        self.applied = applied

class UserClubEventSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'event_id', 'applied')

UserClubEvent_schema = UserClubEventSchema()
UserClubEvents_schema = UserClubEventSchema(many=True)

class UserEvent(db.Model):
    __tablename__ = 'user_event'
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    applied = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, event_id, applied, mainlied=False):
        self.user_id = user_id
        self.event_id = event_id
        self.applied = applied
        self.mainlied = mainlied
        
class UserEventSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'event_id', 'applied')

UserEvent_schema = UserEventSchema()
UserEvents_schema = UserEventSchema(many=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    opt_sk = db.Column(db.String(50), unique=True, default=get_otp_secret_key)
    usn = db.Column(db.String(32))
    username = db.Column(db.String(32))
    admin_role = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(354), unique=True)
    password = db.Column(db.Text, nullable=False)
    ph_number = db.Column(db.Integer) 
    user_events = db.relationship('UserEvent', backref = 'users', lazy=True)
    user_club_events = db.relationship('UserClubEvents', backref='users', lazy=True)
    user_uv_events = db.relationship('UserUVEvents', backref='users', lazy=True)
    event_attendence = db.relationship('EventAttendence', backref='users', lazy=True)


    def __init__(self, usn, email, password, ph_number, username, admin_role):
        self.usn = usn
        self.email = email
        self.password = password
        self.ph_number = ph_number
        self.username = username
        self.admin_role = admin_role

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'ph_number', 'username', 'admin_role')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserNameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')

userName_schema = UserNameSchema()
usersName_schema = UserNameSchema(many=True)


class UserUVEvents(db.Model):
    __tablename__ = "user_uv_events"
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), primary_key=True)
    uv_event_id = db.Column(db.Integer, db.ForeignKey('utsava_vaibhava_events.id'), primary_key=True)
    applied = db.Column(db.Boolean, default=False)
    # user_id = db.Column(db.String(32), db.ForeignKey('users.id'), primary_key=True)

    def __init__(self, user_id, uv_event_id, applied):
        self.user_id = user_id
        self.uv_event_id = uv_event_id
        self.applied = applied

class UserUVEventSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'event_id', 'applied')

User_UV_Event_schema = UserUVEventSchema()
User_UV_Events_schema = UserUVEventSchema(many=True)

class UtsavaVaibhavaEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.LargeBinary, nullable=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.Integer)
    venue = db.Column(db.String(50))
    date = db.Column(db.String(30))
    time = db.Column(db.String(25))
    user_uv_events = db.relationship('User', secondary='user_uv_events', backref='utsava_vaibhava_events', lazy=True)

    def __init__(self, title, description, event_type, amount, venue, date, time):
        # self.image = image
        self.title = title
        self.description = description
        self.event_type = event_type
        self.amount = amount
        self.venue = venue
        self.date = date
        self.time = time

class UtVaiEventsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'event_type', 'amount', 'venue', "date", 'time')

utsava_vaibhava_event_schema = UtVaiEventsSchema()
utsava_vaibhava_events_schema = UtVaiEventsSchema(many=True)

class EventAttendence(db.Model):
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)
    attendence = db.Column(db.Boolean, default=False)

    def __init__(self, user_id, event_id, attendence):
        self.user_id = user_id
        self.event_id = event_id
        self.attendence = attendence

class EventAttendenceSchema(ma.Schema):
    class Meta:
        feilds = ('user_id', 'event_id', 'attendence')

event_attendence_schema = EventAttendenceSchema()
events_attendence_schema = EventAttendenceSchema(many=True)