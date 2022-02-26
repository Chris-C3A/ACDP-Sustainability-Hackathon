import os
import secrets
from PIL import Image
from flask import current_app


def savePostImage(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(current_app.root_path,
                            'static/post_pics', pic_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)

    # form_picture.save(pic_path)
    size = os.path.getsize(pic_path)
    if size > 1000000:
        os.remove(pic_path)
        return False

    return pic_fn


def get_coordinates_of_posts(posts):
    coordinates = []

    for post in posts:
        coord = {}
        coord["longitude"] = post.longitude
        coord["latitude"] = post.latitude

        coordinates.append(coord)
    
    return coordinates
