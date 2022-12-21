"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    '''Redirect to user listing'''
    return redirect('/user-listing')

@app.route('/user-listing')
def user_list():
    '''Show list of users on serparate page'''

    users = User.query.order_by(User.last_name, User.first_name).all()
    
    return render_template('users/index.html', users = users)

@app.route('/user-form', methods = ['GET'])
def show_form():
    '''Show form to create new user'''

    return render_template('user-form.html')

@app.route('/user-form', methods = ['POST'])
def handle_form():
    '''Handle form submission'''

    new_user = User(
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect('/user-listing')

@app.route('/<int:user_id')
def show_user_detail(user_id):
    '''Show page with user info'''

    user = User.query.get(user_id)

    return render_template('user-listing', user = user)

@app.route('/<int:user_id>/user-edit', methods = ['POST'])
def update_user(user_id):
    '''Handle form submission'''

    user = User.query.get(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route('/<int:user_id>/delete', methods = ['POST'])
def remove_user(user_id)
    '''Remove exisiting user'''

    user = User.query.get(user_id)
    db.session.delete(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')


@app.route('/<int:user_id>/posts/new')
def posts_new_form(user_id):

    user = User.query(user_id)
    return render_template('posts/new.html', user=user)

@app.route('/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
   
    user = User.query.get(user_id)
    add_post = Post(title=request.form['title'],
                content=request.form['content'],
                user=user)

    db.session.add(add_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

    @app.route('/posts/<int:post_id>')

def posts_show(post_id):
    
    post = Post.query.get(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):

    post = Post.query.get(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):

    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):

    post = Post.query.get(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")