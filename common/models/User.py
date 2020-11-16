# coding: utf-8
# flask-sqlacodegen.exe 'mysql+pymysql://root@localhost/webapp2' --outfile ./common/models/User.py --flask
from application import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin


# reloading the user from the user_id stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.Text, nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    author_id = db.Column(db.ForeignKey('user.uid'), index=True)

    author = db.relationship('User', primaryjoin='Post.author_id == User.uid', backref='posts')


t_relation = db.Table(
    'relation',
    db.Column('uid', db.BigInteger),
    db.Column('id', db.BigInteger)
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    uid = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    avatar = db.Column(db.String(64), nullable=False, server_default=db.FetchedValue())
    login_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue())
    login_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())

    # 在models.py文件内的O…映射类中添加内置属性id，将uid当做id：
    @property
    def id(self):
        return self.uid

    def get_id(self):
        return self.id

    def get_reset_token(self, expire_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            # 根据传入的token解出原来的字典{'user_id': self.id}
            user_id = s.loads(token)['user_id']
        except:
            return None
        # 将从数据库中根据user_id查到的user返回
        return User.query.get(user_id)
