import os.path,sqlite3,pickle
import json
from flask import render_template, url_for, flash,redirect, request, abort, Blueprint, jsonify, current_app
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import User, Post
from flaskblog.posts.utils import  dict_factory, compare_faces, print_request, detect_emotion
from flaskblog.posts.forms import PostForm, PictureForm
from flaskblog.users.utils import save_picture
from flaskblog.errors.handlers import error_404

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

####################### API TESTING ########################################3

@posts.route('/api/v1/resources/site/all', methods=['GET'])
def api_all():
    db_path = os.path.join(current_app.root_path, 'site.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_site = cur.execute("SELECT * FROM post;").fetchall()

    return jsonify(all_site)

@posts.route('/api/v1/resources/site', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    title = query_parameters.get('title')
    content = query_parameters.get('content')

    query = 'SELECT * FROM post WHERE'
    to_filter = []

    if id:
        query += ' user_id=? AND'
        to_filter.append(id)
    if title:
        query += ' title=? AND'
        to_filter.append(title)
    if content:
        query += ' content=? AND'
        to_filter.append(content)
    if not (id or title or content):
        return error_404(404)

    query = query[:-4] + ';'
    

    conn = sqlite3.connect('site.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()
    

    return jsonify(results)


################## ML MODEL ################################
# @posts.route('/face_match', methods=['GET','POST'])
# def face_match():
#     if request.method == 'POST':
#         print_request(request)        
#         # check if the post request has the file part
#         if 'file' in request.files:
#             file = request.files.get('file')                          
#             name = face_rec(file)    
#             resp_data = {'name': name }
#             return json.dumps(resp_data)      

#     return '''
#     <!doctype html>
#     <title>Face Recognition</title>
#     <h1>Upload an image</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''  
@posts.route('/face_match', methods=['GET','POST'])
@login_required
def face_match():
    form = PictureForm()
    if form.validate_on_submit():
        if form.picture1.data:
            picture_file1 = save_picture(form.picture1.data)
            current_user.pic1 = picture_file1
        db.session.commit()
        
        flash('Your pictures have been posted!', 'success')
        return redirect(url_for('posts.face_match'))
        
    if request.method == 'POST':
        #check if the post request has the file part
        if ('file1' in request.files) and ('file2' in request.files):        
            file1 = request.files.get('file1')
            file2 = request.files.get('file2')                         
            ret = compare_faces(file1, file2)     
            resp_data = {"match": bool(ret)} # convert numpy._bool to bool for json.dumps
            return json.dumps(resp_data)
        
    
    #result = detect_emotion(current_user.pic1)
    pic1= url_for('static', filename='profile_pics/' + current_user.pic1)
    return render_template('emotion_picture.html',title='Emotion Detection', pic1=pic1, form=form)
    

#logic is to post the 2 pics, display them like account pic, save into db, when submitted display resp data