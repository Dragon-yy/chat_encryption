from flask import Blueprint, render_template


route_errors = Blueprint('error_handler', __name__)


@route_errors.app_errorhandler(404)
def error_handler_404(error):
    return render_template('/errors/404.html'), 404


@route_errors.app_errorhandler(403)
def error_handler_403(error):
    return render_template('/errors/403.html'), 403

@route_errors.app_errorhandler(401)
def error_handler_403(error):
    return render_template('/errors/401.html'), 401

@route_errors.app_errorhandler(500)
def error_handler_500(error):
    return render_template('/errors/500.html'), 500
