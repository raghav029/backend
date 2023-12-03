from flask import Blueprint, request
from flask import jsonify
from models import Events, events_schema, event_schema, eventsName_schema
from db.database import db

dept_event = Blueprint("dept_event", __name__)

# ****Events Routes****


# get the dept event
@dept_event.route('/get/deptEvents', methods=['GET'])
def getDeptEvents():
    all_events = Events.query.all()
    results = events_schema.dump(all_events)
    # results.headers.add('Access-Control-Allow-Origin', '*')
    return jsonify(results)
@dept_event.route('/get/deptEvents/names')
def get_dept_events_name():
    all_events_name = Events.query.all()
    return jsonify(eventsName_schema.dump(all_events_name))
    

# get the dept event by id
@dept_event.route("/get/deptEvents/<id>/", methods=['GET'])
def getEventById(id):
    event = Events.query.get(id)
    return event_schema.jsonify(event)



# add an dept event
@dept_event.route('/add/deptEvent/', methods=['POST'])
def add_dept_event():
    # fields = ('image_uri', 'title', 'description', 'event_type', 'venue', "date", 'time', 'event_mode', 'expiration', 'amount', 'dept')
    image_uri = request.json['image_uri']
    title = request.json['title']
    description = request.json['description']
    # dept = request.json['dept']
    event_type = request.json['event_type']
    # amount = request.json['amount']
    venue = request.json['venue']
    date = request.json['date']
    time = request.json['time']
    # event_mode = request.json['event_mode']
    event_mode='individual'

    try:
        event = Events(image_uri=image_uri, title=title, description=description, event_type=event_type, date=date, time=time, event_mode=event_mode, venue=venue, expiration=False, amount=150, dept='ISE')
        db.session.add(event)
        db.session.commit()
    except:
        return jsonify("Event not added"), 401
    
    return event_schema.jsonify(event), 200





# update an event for the corresponsind id
@dept_event.route('/update/deptEvents/<id>/', methods=['PUT'])
def update_event(id):
    event = Events.query.get(id)

    # fields = ('image_uri', 'title', 'description', 'event_type', 'venue', "date", 'time', 'event_mode', 'expiration', 'amount', 'dept')
    image_uri = request.json['image_uri']
    title = request.json['title']
    description = request.json['description']
    dept = request.json['dept']
    event_type = request.json['event_type']
    amount = request.json['amount']
    venue = request.json['venue']
    date = request.json['date']
    time = request.json['time']

    event.image_uri = image_uri
    event.title = title
    event.description = description
    event.dept = dept
    event.event_type = event_type
    event.amount = amount
    event.venue = venue
    event.date = date
    event.time = time

    db.session.commit()

    return event_schema.jsonify(event)

# delete an event for the corresponding id
@dept_event.route("/delete/deptEvent/<id>", methods=['DELETE'])
def deleteAnEvent(id):
    # remove foreign key constrains
        # delete event attendence row for the event id
        # delete user_event relation table row for the event id
    # now delete the event
    
    return jsonify("Event deleted successfully")
