from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from .models import User, Post
from .src.utils import savePostImage


post = Blueprint('post', __name__)


@post.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'GET':
        return render_template('/post/create_post.html')
    elif request.method == 'POST':
        # author = current_user
        caption = request.form.get('caption')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')


        uploaded_image = request.files['file']
        post_image = savePostImage(uploaded_image)

        if post_image:
            # creates new post
            new_post = Post(caption=caption, longitude=longitude, latitude=latitude, image_file=post_image, author=current_user)
            
            db.session.add(new_post)
            db.session.commit()

            flash('Post successfully created', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Image size too large! Please use a different image', 'danger')
            return redirect(url_for('post.new_post'))


@post.route('/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # check if use trying to delete the post is the author of the post
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been successfully deleted', 'success')
    return redirect(url_for('main.profile'))
