from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment, PostLike
from flaskblog.posts.forms import PostForm
from flaskblog.comments.forms import CommentForm
from flaskblog.users.utils import save_picture, remove_picture



posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        print(form.image.data)
        if form.image.data:
            post_image = save_picture(form.image.data, directory='static/post_image')
            post = Post(title=form.title.data, content=form.content.data, author=current_user, image_file=post_image)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)   
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template("posts/create_post.html", title = "New Post", 
                            form = form, legend="New Post")


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data, author_id=current_user.id, post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been published!', 'success')
            return redirect(url_for('posts.post', post_id=post.id))
        else:
            flash('You need to login to write comments!', 'danger')

    comments_of_post = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_commented.desc()).all()
    
    return render_template("posts/post.html", title = post.title, post = post, form = form, comments = comments_of_post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        if form.image.data:
            post_image = save_picture(form.image.data, directory='static/post_image')
            # if post alredy has image, remove it
            if post.image_file:
                old_image = post.image_file
                remove_picture(old_image, directory='static/post_image')
            post.image_file = post_image
            
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id = post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template("posts/create_post.html", title = "Update Post", 
                            form = form, legend="Update Post")


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    # before deleting the post, delete its comments
    Comment.query.filter_by(post_id=post.id).delete()

    # before deleting the post, delete its likes
    PostLike.query.filter_by(post_id=post.id).delete()

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))









