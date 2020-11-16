from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user
from web.forms import RequestResetForm, ResetPasswordForm
from common.models.User import User
from application import mail, db
from flask_mail import Message
from common.libs.passwd_gen import passwd_gen

route_reset_request = Blueprint('reset_request', __name__)
route_reset_token = Blueprint('reset_token', __name__)


def send_reset_email(user):
    token = user.get_reset_token()
    # 这里的sender注意
    msg = Message('Password Reset Request',
                  sender='623852374@qq.com',
                  recipients=[user.email])
    # _external=True是为了显示绝对的url地址
    msg.body = f'''To reset your password, visit the following link\n
重置你的密码请点击如下链接\n
{url_for('reset_token.reset_token', token=token, _external=True)}\n
If you did not make this request ,please just ignore this email\n
如果不是你本人的操作，请忽略这份邮件\n
'''
    mail.send(msg)


@route_reset_request.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # 如果当前用户已经登陆就不可能需要重置密码（直接redirect到home）
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # 根据表单传上来的Email找到user对象
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user=user)
        flash('An email has been sent with instructions to reset your password', category='info')
        return redirect(url_for('login.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@route_reset_token.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    # 如果当前用户已经登陆就不可能需要重置密码（直接redirect到home）
    if current_user.is_authenticated:
        return redirect(url_for('home.home'))
    user = User.verify_reset_token(token=token)
    if user is None:
        flash('That is an invalid or expired token', category='warning')
        return redirect(url_for('reset_request.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        import random
        # 生成盐(用来给密码加密)可以用python自带的secrets
        salt = ''.join([random.choice('0123456789abcdefABCDEF') for i in range(12)])
        # 将数据库中的login_pwd 和login_salt 更新
        user.login_pwd = passwd_gen(pwd=form.password.data, salt=salt)
        user.login_salt = salt
        db.session.commit()
        flash(message='Your password has been updated!', category='success')
        return redirect(url_for('login.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
