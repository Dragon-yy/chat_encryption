from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user
from application import app, db
from web.forms import PostForm
from common.models.User import Post
from datetime import datetime

route_post = Blueprint('new_post', __name__)
route_post_id = Blueprint('post', __name__)
# route_post_update = Blueprint('post_update', __name__)
# route_post_delete = Blueprint('post_delete', __name__)


@route_post.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm(csrf_secret=app.config['SECRET_KEY'])
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    created_time=datetime.utcnow())
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", category='success')
        return redirect(url_for('home.home'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=form)


@route_post_id.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@route_post_id.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    # 从数据库中拿到的数据（post）
    post = Post.query.get_or_404(post_id)
    # 如果修改post不是提交post的用户abort
    if post.author != current_user:
        abort(403)

    # 从表单中拿到数据（form）
    form = PostForm(csrf_secret=app.config['SECRET_KEY'])
    # 如果表单提交成功 将数据库中的post数据改为表单提交的数据
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        # 因为数据库中已经有了post数据所以不用再调用方法add
        db.session.commit()
        flash('Your post has been updated', category='success')
        return redirect(url_for('post.post', post_id=post.id))
    elif request.method == 'GET':
        # 如果表单提交不成功 将数据库中的数据赋值给表单
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_post.html', title='Update Post', legend='Update Post', form=form)


@route_post_id.route('/post/<int:post_id>/delete', methods=[ 'POST'])
@login_required
def post_delete(post_id):
    # 从数据库中拿到的数据（post）
    post = Post.query.get_or_404(post_id)
    # 如果修改post不是提交post的用户abort
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', category='danger')
    return redirect(url_for('home.home'))

