from flask import Blueprint, jsonify
from models import user_schema, users_schema, UserEvent, UserClubEvents, User, Events, usersName_schema

eu = Blueprint("events_user", __name__)

@eu.route('/get/eventparticipants/<id>/')
def get_event_applicants(id):
    # get the id of events
    event_id = id
    #retrive all the users applied for the event
    event_users = UserEvent.query.filter(UserEvent.event_id==event_id).all()
    if not event_users:
        return jsonify("Event doesn't exist")

    #retrive user details for event_users
    user_ids = [user_event.user_id for user_event in event_users]
    all_users = User.query.filter(User.id.in_(user_ids)).all()

    users_data = users_schema.dump(all_users)

    return jsonify(users_data)


@eu.route('/get/eventparticipants/name/<id>/')
def get_event_applicants_name(id):
    # get the id of the event
    event_id = id
    # retrive all the applicants applied
    event_participants = UserEvent.query.filter(UserEvent.event_id==event_id).all()
    if not event_participants:
        return jsonify("Event doesn't exist")
    
    #retrive user details for event_users
    user_ids = [user_event.user_id for user_event in event_participants]
    all_users = User.query.filter(User.id.in_(user_ids)).all()

    users_data = usersName_schema.dump(all_users)

    return jsonify(users_data)


#end DEPT events for all users routes
# details of users mainlied for specific CLUB events
@eu.route('/get/clubEventapplied/<id>/')
def get_club_event_users(id):
    # get the id of the event
    club_event_id = id
    # retirve all the users associated with the event
    event_users = UserClubEvents.query.filter(UserClubEvents.club_event_id==club_event_id).all()

    if not event_users:
        return jsonify("Event doest Exist")
    
    # retrive user details for the event_users
    user_ids = [user_club_event.user_id for user_club_event in event_users]
    all_users = User.query.filter(User.id.in_(user_ids)).all()

    user_data = users_schema.dump(all_users)

    return jsonify(user_data)