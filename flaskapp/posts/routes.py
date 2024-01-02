from flaskapp.models import Post
from flask import render_template, url_for, flash,redirect, request, Blueprint
from flaskapp import db
from flaskapp.posts.forms import NoteForm
from flask_login import current_user, login_required
from flaskapp.main.utils import the_device
from datetime import datetime

posts = Blueprint('posts', __name__)

@posts.route("/note/new", methods=["GET", "POST"])
@login_required
def new_note():
        form = NoteForm()
        if form.validate_on_submit():
                post = Post(title=form.title.data, content=form.content.data, author=current_user)
                db.session.add(post)
                db.session.commit()
                flash("Your note has been added!", "success")
                return redirect(url_for("main.home"))
        if the_device():
                return render_template("addnotes-mobile.html", title="NEWNOTE-MOBILE", form=form, device=the_device())
        else:
                return render_template("addnotes.html", title="NEWNOTE", form=form,device=the_device())

@posts.route("/post/<int:post_id>")
def post(post_id):
        post = Post.query.get_or_404(post_id)
        if the_device():
                return render_template("viewnote-mobile.html", title="View Note-Mobile", post=post, device=the_device())
        else:
                return render_template("viewnote.html", title="View Note", post=post, device=the_device())

@posts.route("/post/<int:post_id>/u",methods=["GET", "POST"])
@login_required
def update_post(post_id):
        post = Post.query.get_or_404(post_id)
        form = NoteForm()
        if form.validate_on_submit():
                post.title = form.title.data
                post.content = form.content.data
                post.date_posted = datetime.utcnow()
                db.session.commit()
                flash("Your post has been updated!", "success")
                return redirect(url_for("posts.post", post_id=post.id))
        elif request.method == "GET":
                form.title.data = post.title
                form.content.data = post.content
        if the_device():
                return render_template("addnotes-mobile.html", title="Update Post-Mobile", form=form, device=the_device())
        else:
                return render_template("addnotes.html", title="Update Post", form=form, device=the_device())

@posts.route("/post/<int:post_id>/d",methods=["POST"])
@login_required
def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash("Your post has been deleted!", "success")
        return redirect(url_for("main.home"))