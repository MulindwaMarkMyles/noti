from flask import render_template, request, Blueprint, url_for
from flaskapp import login_manager
from flaskapp.models import Post
from flask_login import current_user, login_required
from flaskapp.main.forms import SearchForm
from flaskapp.main.utils import the_device

main = Blueprint('main', __name__)

@main.route("/home",methods=["GET","POST"])
@main.route("/",methods=["GET","POST"])
@login_required
def home():
        image_file = url_for('static', filename=f"images/{current_user.image_file}")
        form = SearchForm()
        posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).all()
        if request.method == "GET":
                if the_device():
                        return render_template("index-mobile.html",title="HOME-MOBILE", image_file=image_file, posts=posts, form=form, device=the_device())
                else:
                        return render_template("index.html",title="HOME", image_file=image_file, posts=posts, form=form, device=the_device())
        elif request.method == "POST":
                search_results = []
                for item in posts:
                        if item.title.lower().__contains__(form.searchterm.data) or item.content.lower().__contains__(form.searchterm.data):
                                search_results.append(item)
                if the_device():
                        return render_template("index-mobile.html",title="HOME-MOBILE", image_file=image_file, posts=search_results, form=form, device=the_device())
                else:
                        return render_template("index.html",title="HOME", image_file=image_file, posts=search_results, form=form, device=the_device())

@main.route("/about")
def about():
        return '<h1 style="font-family:\'Poppins\'"> The about Page ! 😁 </h1>'
