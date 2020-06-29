from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=5)
    return render_template("main/home.html", posts=posts)


@main.route('/about')
def about():
    return render_template("main/about.html", title="About")


@main.route('/mycv')
def mycv():
    return render_template("main/mycv.html", title="My CV")


@main.route('/article/working_with_remote_server')
def working_with_remote_server():
    return render_template("main/articles/working_with_remote_server.html",
                           title="Working_with_remote_server")
