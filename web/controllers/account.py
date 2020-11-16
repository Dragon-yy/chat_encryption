from flask import Blueprint, render_template, url_for, flash, redirect
from flask_login import login_required, current_user
from web.forms import UpdateAccountForm
from application import app, db
from PIL import Image
from PIL.Image import EXTENT
route_account = Blueprint('account', __name__)


def save_avatar(form_avatar):
    import os
    import secrets
    random_hex = secrets.token_hex(8)
    # 将从表单上传的图片文件切割成文件名+扩展名的形式
    _, file_ext = os.path.splitext(form_avatar.filename)
    avatar_name = random_hex + file_ext
    # 构造上传文件路径
    avatar_path = os.path.join(app.root_path+'/web/static/user_pics/'+avatar_name)

    # resize the image
    output_size = (34, 34)
    img = Image.open(form_avatar)
    offset = int(img.size[0] - img.size[1]) / 2
    img = img.transform(output_size, EXTENT, (offset, 0, int(img.size[0]-offset), img.size[1]))
    img.save(avatar_path)
    return avatar_name


@route_account.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(csrf_secret=app.config['SECRET_KEY'])
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_name = save_avatar(form.avatar.data)
            current_user.avatar = avatar_name
        form.validate_username(form.username)
        form.validate_email(form.email)
        current_user.login_name = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been successfully updated !', category='success')
        return redirect(url_for('account.account'))
    avatar = '../static/user_pics/'+current_user.avatar
    app.logger.info('--------------'+avatar)
    return render_template('account.html',
                           title='Account',
                           avatar=avatar,
                           form=form)
