from flask import render_template, redirect, url_for, flash, request, abort, Blueprint
from flaskblog import db
from flaskblog.posts.forms import NewPostForm
from flaskblog.models import Post
from flask_login import current_user, login_required


posts = Blueprint('posts', __name__)

@posts.route('/add-post', methods=['GET', 'POST'])
@login_required
def addPost():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your new post is created successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template('add_post.html', form=form)

@posts.route('/update-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = NewPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Your post is updated successfully', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_post.html', form=form)

@posts.route('/delete-post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post is deleted successfully', 'success')
    return redirect(url_for('main.home'))