from flask import Blueprint
from flask import jsonify
from models import Events
import base64

image = Blueprint("image_poster", __name__)

@image.route('/get/image_data/<id>/')
def image_data(id):
    image = Events.query.filter(Events.id==id).first()
    # encoding the image to base64 for sending it to frontend
    image_base64 = base64.b64encode(image).decode('utf-8')
    response = {
        "image":image_base64,
        "image_name": image.image_file_name
    }
    return jsonify(response)