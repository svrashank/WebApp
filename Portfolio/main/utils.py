from Portfolio import app
import secrets
import os 
from Portfolio import app
from flask import request
from urllib.parse import urlparse, urljoin
import secrets
import os 

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(app.root_path,"static/profile_pics",picture_filename)
    form_picture.save(picture_path)
    # output_size = (125,125)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)
    return picture_filename

def save_resume(form_resume_file):
    random_hex = secrets.token_hex(8)
    _,file_ext = os.path.splitext(form_resume_file.filename)
    resume_filename = random_hex + file_ext
    file_path = os.path.join(app.root_path,"static/resume",resume_filename)
    form_resume_file.save(file_path)
    return 


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc