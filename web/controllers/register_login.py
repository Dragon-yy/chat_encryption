from flask import Blueprint, render_template, flash, redirect, url_for
from application import app, db
from web.forms import RegistrationForm, LoginForm
from common.models.User import User
from common.libs.passwd_gen import passwd_gen
from flask_login import login_user, current_user, login_required

route_register = Blueprint('register', __name__)
route_login = Blueprint('login', __name__)


# 注册逻辑
@route_register.route('/register', methods=['GET', 'POST'])
def register():
    # 如果用户已经登入就没必要注册（直接重定向到home)
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    # 创建表单对象
    form = RegistrationForm(csrf_secret=app.config['SECRET_KEY'])
    if form.validate_on_submit():
        import random
        # 生成盐(用来给密码加密)可以用python自带的secrets
        salt = ''.join([random.choice('0123456789abcdefABCDEF') for i in range(12)])
        form.validate_username(form.username)
        form.validate_email(form.email)
        # 创建User对象将提交上来的注册表单数据放在user_info中
        user_info = User(login_name=form.username.data,
                         email=form.email.data,
                         login_pwd=passwd_gen(form.password.data, salt),
                         login_salt=salt)
        # 向数据库插入 user_info
        db.session.add(user_info)
        db.session.commit()
        flash(message=f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('login.login'))
    return render_template('register.html', title='Registration', form=form)


# 登陆逻辑
@route_login.route('/login', methods=['GET', 'POST'])
def login():
    # 如果用户已经登入过就没必要再登入（直接重定向到home)
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    # 创建表单对象
    form = LoginForm(csrf_secret=app.config['SECRET_KEY'])
    if form.validate_on_submit():
        # 数据库查询
        user_info = User.query.filter_by(email=form.email.data).first()
        if user_info and user_info.login_pwd == passwd_gen(form.password.data, user_info.login_salt):
            # login_user 是为了从user_info中得到id ，再将id放到session中
            login_user(user_info, remember=form.remember.data)
            flash(message=f'You have been successfully login in !', category='success')
            return redirect(url_for('home.home'))
        else:
            flash(message=f'Please recheck your email and password !', category='danger')

    return render_template('login.html', title='Login', form=form)
