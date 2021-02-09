"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def create_user_form():
    return render_template('create_user.html')

@app.route('/users/new', methods=['POST'])
def create_user():
    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    image_url = request.form.get('image_url', None)
    if (first_name and last_name):
        new_user = User(first_name = first_name, last_name=last_name, image_url=image_url if image_url else None)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/users/new')

@app.route('/users/<int:id>')
def user_detail(id):
    user = User.query.get_or_404(id)
    if (user):
        posts = user.posts
    return render_template('user_detail.html', user=user, posts = posts)

@app.route('/users/<int:id>/edit')
def user_edit(id):
    user = User.query.get_or_404(id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def user_edit_process(id):
    user = User.query.get_or_404(id)
    first_name = request.form.get('first_name', None)
    last_name = request.form.get('last_name', None)
    image_url = request.form.get('imgage_url', None)
    if (first_name):
        user.first_name = first_name
    if (last_name):
        user.last_name = last_name
    if (image_url):
        user.image_url = image_url
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:id>/delete', methods=['POST'])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
    
@app.route('/users/<int:id>/posts/new')
def create_post(id):
    user = User.query.get_or_404(id)
    available_tags = Tag.query.all()
    return render_template('create_post.html', user = user, available_tags=available_tags)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def create_post_process(id):
    user = User.query.get(id)
    if (user):
        title = request.form.get('title', None)
        content = request.form.get('content', None)
        tag_ids = request.form.getlist('tag_ids')
        if (title and content):
            new_post = Post(title=title, content=content, user_id=id)
            for tag_id in tag_ids:
                tag = Tag.query.get_or_404(tag_id)
                new_post.tags.append(tag)
            db.session.add(new_post)
            db.session.commit()
            return redirect(f'/posts/{new_post.id}')
    return redirect(f'/users/{id}/posts/new')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user
    tags = post.tags
    return render_template('post_detail.html', user=user, post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post_process(post_id):
    post = Post.query.get_or_404(post_id)
    title = request.form.get('title', None)
    content = request.form.get('content', None)
    if (title or content):
        post.title = title or post.title
        post.content = content or post.content
        db.session.add(post)
        db.session.commit()
        return redirect(f'/posts/{post_id}')
    else:
        return redirect(f'/posts/{post_id}/edit')
    
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')

# GET /tags
# Lists all tags, with links to the tag detail page.
@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

# GET /tags/[tag-id]
# Show detail about a tag. Have links to edit form and to delete.
@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tagged_posts = tag.posts
    return render_template('tag_detail.html', tag=tag, tagged_posts=tagged_posts)

# GET /tags/new
# Shows a form to add a new tag.
@app.route('/tags/new')
def tag_new():
    return render_template('tag_new.html')

# POST /tags/new
# Process add form, adds tag, and redirect to tag list.
@app.route('/tags/new', methods=['POST'])
def tag_new_post():
    tag_name = request.form.get('name', None)
    if (tag_name):
        tag = Tag(name=tag_name)
        db.session.add(tag)
        db.session.commit()
        return redirect('/tags')
    else:
        return render_template('tag_new.html')

# GET /tags/[tag-id]/edit
# Show edit form for a tag.
@app.route('/tags/<int:tag_id>/edit')
def tag_edit_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_edit.html', tag=tag)

# POST /tags/[tag-id]/edit
# Process edit form, edit tag, and redirects to the tags list.
@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def tag_edit_process(tag_id):
    tag_name = request.form.get('name', None)
    if (tag_name):
        tag = Tag.query.get_or_404(tag_id)
        tag.name = tag_name
        db.session.add(tag)
        db.session.commit()
        return redirect('/tags')
    else:
        return redirect(f'/tags/{tag_id}/edit')
# POST /tags/[tag-id]/delete
# Delete a tag.
@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tag_delete(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
    
