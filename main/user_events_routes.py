from flask import Blueprint, jsonify, request, session
from models import UserEvent, UserEvent_schema, Events, events_schema, UserClubEvents, UserClubEvent_schema, UserUVEvents, User_UV_Event_schema, ClubEvents, club_events_schema, utsava_vaibhava_events_schema, UtsavaVaibhavaEvents


from db.database import db

ue = Blueprint("user_events", __name__)

# ****user-events routes****
# Dept-User-Event Routes
@ue.route('/apply/userEvents', methods=['POST'])
def apply_user_events():
    user_id = session.get('user_id')
    # check if user exist
    if not user_id:
        return jsonify("Unauthorised asscess"), 401
    
    # get the event id
    event_id = request.json['event_id']

    user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
    if user_event:
        user_event.applied = True
    else:
        user_event = UserEvent(user_id=user_id, event_id=event_id, applied=True,mainlied=True)
        db.session.add(user_event)
    
    db.session.commit()

    return UserEvent_schema.jsonify(user_event)

@ue.route('/getUserEvents')
def get_current_user_events():
    user_id = session.get('user_id')
    # check if user exist
    if not user_id:
        return jsonify("Unauthorised asscess"), 401
    # retrieve all the events user applied for
    user_events = UserEvent.query.filter(UserEvent.user_id == user_id).all()

    if not user_events:
        return jsonify("No events selected")
    
    # retrieve events details for each user_event
    event_ids = [user_event.event_id for user_event in user_events]
    all_events = Events.query.filter(Events.id.in_(event_ids)).all()

    event_data = events_schema.dump(all_events)

    return jsonify(event_data)
# get event ids for the mainlied events
@ue.route('/getUserEventsIds')
def get_current_user_events_ids():
    user_id = session.get('user_id')
    # check if user exist
    if not user_id:
        return jsonify("Unauthorised asscess"), 401
    # retrieve all the events user mainlied for
    user_events = UserEvent.query.filter(UserEvent.user_id == user_id).all()

    if not user_events:
        return jsonify("No events selected")
    
    # retrieve events details for each user_event
    event_ids = [user_event.event_id for user_event in user_events]
    all_events = Events.query.filter(Events.id.in_(event_ids)).all()
    mainlied_event_ids = [event.id for event in all_events]

    return jsonify(mainlied_event_ids)
# end get event ids
# end dept-user-events routes

# Club-User-Events Routes
@ue.route('/UserClubEvent', methods=['POST'])
def clubEvents():
    user_id = session.get('user_id')
    # check if user exist
    if not user_id:
        return jsonify("Unauthorised access"), 401
    # get the event id
    club_event_id = request.json['club_event_id']

    user_event = UserClubEvents.query.filter_by(user_id=user_id, club_event_id=club_event_id).first()
    if user_event:
        user_event.mainlied = True
    else:
        user_event = UserClubEvents(user_id=user_id, club_event_id=club_event_id, mainlied=True)
        db.session.add(user_event)
    db.session.commit()
    return UserClubEvent_schema.jsonify(user_event)

@ue.route('/getUserClubEvents')
def getUserClubEvents():
    user_id = session.get('user_id')
    # check if user exist
    if not user_id:
        return jsonify("Unauthorised access"), 401
    # retrive all the events mainlied by the user
    user_events = UserClubEvents.query.filter(UserClubEvents.user_id == user_id).all()

    if not user_events:
        return jsonify("no events mainlied")
    
    # retrieve events details for that user
    event_ids = [userClubEvent.club_event_id for userClubEvent in user_events]
    all_events = ClubEvents.query.filter(ClubEvents.id.in_(event_ids)).all()

    event_data = club_events_schema.dump(all_events)
    return jsonify(event_data)
# end Club-User-Events Routes
# uv-user-event routes
@ue.route('/userUVevents', methods=['POST'])
def UVevents():
    user_id = session.get('user_id')
    # check if user exists
    if not user_id:
        return jsonify("Unauthorised access"), 401
    # get the event id
    uv_event_id = request.json['uv_event_id']

    user_event = UserUVEvents.query.filter_by(user_id=user_id, uv_event_id=uv_event_id).first()
    if user_event:
        user_event.mainlied = True
    else:
        user_event = UserUVEvents(user_id=user_id, uv_event_id=uv_event_id, mainlied=True)
        db.session.add(user_event)
    
    db.session.commit()
    return User_UV_Event_schema.jsonify(user_event)

@ue.route('/get/uvUserEvents')
def get_user_uv_events():
    user_id = session.get('user_id')
    # check if user exist
    if not user_id:
        return jsonify("Unauthorised access"), 401
    # retirve events for the user mainlied for
    user_events = UserUVEvents.query.filter(UserUVEvents.user_id==user_id).all()

    if not user_events:
        return jsonify("No events mainlied")
    
    # retirve events details for that user
    event_ids = [userUVevent.uv_event_id for userUVevent in user_events]
    all_events = UtsavaVaibhavaEvents.query.filter(UtsavaVaibhavaEvents.id.in_(event_ids)).all()

    event_data = utsava_vaibhava_events_schema.dump(all_events)
    return jsonify(event_data)
# end uv-user-event-routes