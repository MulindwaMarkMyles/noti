from flask import render_template, request, Blueprint, url_for
from flaskapp import login_manager
from flaskapp.models import Post
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route("/home")
@main.route("/")
@login_required
def home():
        image_file = url_for('static', filename=f"images/{current_user.image_file}")
        posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).all()
        return render_template("index.html",title="HOME", image_file=image_file, posts=posts)


@main.route("/about")
def about():
        return "About Page!"
