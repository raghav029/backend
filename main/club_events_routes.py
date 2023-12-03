from flask import Blueprint, jsonify, request
from models import club_event_schema, ClubEvents, club_events_schema
from db.database import db

club_event = Blueprint("club_events", __name__)

# get club events
@club_event.route('/get/clubEvents')
def getClubEvents():
    all_events = ClubEvents.query.all()
    result = club_events_schema.dump(all_events)
    return jsonify(result)

@club_event.route('/get/clubEvents/<id>')
def getClubEventById(id):
    event = ClubEvents.query.get(id)
    return club_event_schema.jsonify(event)

@club_event.route('/add/clubEvents', methods=['POST'])
def add_club_events():
    # image = request.json['image']
    title = request.json['title']
    description = request.json['description']
    club = request.json['club']
    event_type = request.json['event_type']
    amount = request.json['amount']
    venue = request.json['venue']
    date = request.json['date']
    time = request.json['time']

    club_event = ClubEvents(title, description, club, event_type, amount, venue, date, time)
    db.session.add(club_event)
    db.session.commit()
    return club_event_schema.jsonify(club_event)

@club_event.route('/update/clubEvents/<id>', methods=['PUT'])
def update_event(id):
    event = ClubEvents.get(id)

    #  image, title, description, club, event_type, amount, venue, date, time
    # image = request.json['image']
    title = request.json['title']
    description = request.json['description']
    club = request.json['club']
    event_type = request.json['event_type']
    amount = request.json['amount']
    venue = request.json['venue']
    date = request.json['date']
    time = request.json['time']

    # club_events.image = image
    title = title
    description = description
    club = club
    event_type = event_type
    amount = amount
    venue = venue
    date = date
    time = time

    db.session.commit()

    return club_event_schema.jsonify(event)