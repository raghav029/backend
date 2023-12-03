from flask import Blueprint, jsonify, request
from db.database import db
from models import Events, User, EventAttendence, event_attendence_schema, users_schema, events_schema, usersName_schema

attendence = Blueprint('event_attendence', __name__)

@attendence.route('/post/event_attendence/', methods=["POST"])
def post_attendence():
    # get the event id
    event_id = request.json['event_id']
    # check if event exist
    event = Events.query.filter_by(id=event_id).first()
    if not event:
        return jsonify("Event doest exist"), 401
    # get the user ids
    user_ids = request.json['user_ids']
    # declaring variables
    invalid_user_ids = []
    attendance_given = []
    # check if attendece already given
    for user_id in user_ids:
        user = User.query.filter(User.id == user_id).first()
        if not user:
            invalid_user_ids.append(user_id)
            continue

        event_attendance = EventAttendence.query.filter_by(event_id=event_id, user_id=user_id).first()
        if event_attendance:
            attendance_given.append(user_id)
            continue

        event_attendance = EventAttendence(event_id=event_id, user_id=user_id, attendence=True)
        db.session.add(event_attendance)

    db.session.commit()

    response_data = {}

    if invalid_user_ids:
        response_data["invalid_user_ids"] = invalid_user_ids

    if attendance_given:
        response_data["attendance_given"] = attendance_given

    if response_data:
        jsonify(response_data), 403

    return event_attendence_schema.jsonify(event_attendance), 200

@attendence.route("/get/event/attnedence", methods=["POST"])
def get_event_attendence():
    event_id = request.json['event_id']
    # get event details corresponding to that id
    event = Events.query.filter_by(id=event_id).first()
    if not event:
        return jsonify("event doest exist"), 401
    # retirve all the users attended the event
    users_attended = EventAttendence.query.filter(EventAttendence.event_id==event_id).all()
    if not users_attended:
        return jsonify("no attendence"), 402

    # retrive all users for that event_id
    user_ids = [user_attended.user_id for user_attended in users_attended]
    all_users = User.query.filter(User.id.in_(user_ids)).all()

    users_data = usersName_schema.dump(all_users)

    return jsonify(users_data)

@attendence.route('/get/user/allAttendedEvents', methods=['post'])
def get_user_all_attended_events():
    user_name = request.json['user_name']
    # get user details
    user = User.query.filter(User.username==user_name).first()

    if not user:
        return jsonify("user doesn't exist"), 401
    # get the user id
    user_id = user.id
    # retirve all events associated with that user user_id
    events = EventAttendence.query.filter(EventAttendence.user_id==user_id).all()
    # check if user attended any event
    if not events:
        return jsonify("User didn't attend any event"), 402
    # retirve all event ids
    event_ids = [event.event_id for event in events]
    all_events = Events.query.filter(Events.id.in_(event_ids)).all()

    events_data = events_schema.dump(all_events)
    return jsonify(events_data)
    

