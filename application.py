from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO
import os


class Application(Flask):
    def __init__(self, import_name, template_folder, static_folder, root_path):
        super(Application, self).__init__(import_name,
                                          template_folder=template_folder,
                                          static_folder=static_folder,
                                          root_path=root_path)
        # 导入基本配置
        self.config.from_pyfile('./config/basic_setting.py')
        # 导入个性化配置
        if 'ops_config' in os.environ:
            self.config.from_pyfile('./config/%s_setting.py' % (os.environ['ops_config']))
        self.config['SECRET_KEY'] = '897109005f7b4fa01c9b00775bddecf2'
        # 邮箱配置
        self.config['MAIL_SERVER'] = 'smtp.qq.com'
        self.config['MAIL_PORT'] = 25
        self.config['MAIL_USER_TLS'] = True
        self.config['MAIL_USERNAME'] = '623852374@qq.com'
        self.config['MAIL_PASSWORD'] = 'yutrhsiudilsbdgf'
        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__,
                  template_folder=os.getcwd()+'/web/templates/',
                  static_folder=os.getcwd()+'/web/static/',
                  root_path=os.getcwd())
manage = Manager(app)
# 在后端处理各种session
login_manager = LoginManager(app)
# 邮箱用于重置密码
mail = Mail(app)

socketio = SocketIO(app)
