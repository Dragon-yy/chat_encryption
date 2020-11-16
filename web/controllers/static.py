from flask import Blueprint, send_from_directory
from application import app


route_static = Blueprint('static', __name__)


@route_static.route('/<path:filename>')
def static(filename):
    app.logger.info('---------------------'+app.root_path + "/web/"+filename)
    return send_from_directory(app.root_path + "/web/", filename)
