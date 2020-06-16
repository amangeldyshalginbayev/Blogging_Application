from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment
from flaskblog.comments.forms import CommentForm, UpdateCommentForm



comments = Blueprint('comments', __name__)


@comments.route('/comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def update_delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)
    form = UpdateCommentForm()

    if form.validate_on_submit():
        if form.update.data:
            comment.content = form.content.data
            db.session.commit()
            flash('Your comment has been updated', 'success')
            return redirect(url_for('posts.post', post_id=comment.post_id))
        elif form.delete.data:
            db.session.delete(comment)
            db.session.commit()
            flash('Your comment has been deleted!', 'success')
            return redirect(url_for('posts.post', post_id=comment.post_id))
    elif request.method == 'GET':
        form.content.data = comment.content

    return render_template("comments/comment.html", comment = comment, form = form)





