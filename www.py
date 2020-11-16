from web.controllers.home import route_home, route_user
from web.controllers.register_login import route_register, route_login
from web.controllers.static import route_static
from web.controllers.logout import route_logout
from web.controllers.account import route_account
from web.controllers.reset import route_reset_token, route_reset_request
from web.controllers.error_handler import route_errors
from application import app


app.register_blueprint(route_home, prefix='/')
app.register_blueprint(route_register, prefix='/register')
app.register_blueprint(route_login, prefix='/login')
app.register_blueprint(route_static, prefix='/static')
app.register_blueprint(route_logout, prefix='/logout')
app.register_blueprint(route_account, prefix='/account')
app.register_blueprint(route_user, prefix='/user')
app.register_blueprint(route_reset_request, prefix='/reset_password')
app.register_blueprint(route_reset_token, prefix='/reset_password')
app.register_blueprint(route_errors, prefix='/errors')
