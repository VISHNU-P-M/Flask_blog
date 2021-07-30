from flask import render_template, Blueprint
from flaskblog.models import Post


main = Blueprint('main', __name__)

@main.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts = posts)
