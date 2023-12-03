from flask import Blueprint, jsonify, request
from models import utsava_vaibhava_event_schema, UtsavaVaibhavaEvents, utsava_vaibhava_events_schema
from db.database import db

uv_events = Blueprint("uv_events", __name__)

# get utsava-vaibhava events
@uv_events.route('/get/uvEvents')
def getUVEvents():
    events = UtsavaVaibhavaEvents.query.all()
    result = utsava_vaibhava_events_schema.dump(events)
    return jsonify(result)

@uv_events.route('/get/uvEvents/<id>')
def getUVEventById(id):
    event = UtsavaVaibhavaEvents.query.get(id)
    return utsava_vaibhava_event_schema.jsonify(event)

@uv_events.route('/add/uvEvents', methods=['POST'])
def add_uv_events():
    # image = request.json['image']
    title = request.json['title']
    description = request.json['description']
    event_type = request.json['event_type']
    amount = request.json['amount']
    venue = request.json['venue']
    date = request.json['date']
    time = request.json['time']

    uv_event = UtsavaVaibhavaEvents(title, description, event_type, amount, venue, date, time)
    db.session.add(uv_event)
    db.session.commit()
    return utsava_vaibhava_event_schema.jsonify(uv_event)