from flask import render_template, request, Blueprint, url_for
from flaskapp import login_manager
from flaskapp.models import Post
from flask_login import current_user, login_required
from flaskapp.main.forms import SearchForm

main = Blueprint('main', __name__)

@main.route("/home",methods=["GET","POST"])
@main.route("/",methods=["GET","POST"])
@login_required
def home():
        image_file = url_for('static', filename=f"images/{current_user.image_file}")
        form = SearchForm()
        posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.date_posted.desc()).all()
        if request.method == "GET":
                return render_template("index.html",title="HOME", image_file=image_file, posts=posts, form=form)
        elif request.method == "POST":
                search_results = []
                for item in posts:
                        print(item.title)
                        if item.title.lower().__contains__(form.searchterm.data) or item.content.lower().__contains__(form.searchterm.data):
                                search_results.append(item)
                return render_template("index.html",title="HOME", image_file=image_file, posts=search_results, form=form)

@main.route("/about")
def about():
        return '<h1 style="font-family:\'Poppins\'"> The about Page ! 😁 </h1>'
