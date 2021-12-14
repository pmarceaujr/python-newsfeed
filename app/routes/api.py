from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()
  db =get_db()
  
  try:
    #Create new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )  
    print(data)    

    # Save new user record to the DB
    db.add(newUser)
    db.commit()
    print('success!')

  except AssertionError:
    print('validation error')
  except sqlalchemy.exc.IntegrityError:
    print('mysql error')
  except:
    # insert failed, so send error to front end
    print(sys.exc_info()[0])
    # insert failed, so rollback and send error to front end
    db.rollback()    
    return jsonify(message = 'Signup failed'), 500

  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])

  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True
  return jsonify(id = user.id)

@bp.route('/comments', methods=['POST'])
def comment():
  data = request.get_json()
  db =get_db()
  
  try:
    #Create new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )  
    print(data)    

    # Save new user record to the DB
    db.add(newComment)
    db.commit()

  except:
    # insert failed, so send error to front end
    print(sys.exc_info()[0])
    # insert failed, so rollback and send error to front end
    db.rollback()    
    return jsonify(message = 'Add comment failed'), 500

 # session.clear()
 # session['user_id'] = newUser.id
 # session['loggedIn'] = True

  return jsonify(id = newComment.id)  

@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
  data = request.get_json()
  db =get_db()

  try:
    #create a new upvote for the post
    newVote = Vote(post_id = data['post_id'],
    user_id = session.get('user_id')
    )

    # Save new upvote to the DB
    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])
    db.rollback()
    return jsonify(message = 'Upvote failed'), 500
  return '', 204   

@bp.route('/posts', methods=['POST'])
def create():
  data = request.get_json()
  db =get_db()
  
  try:
    #Create new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )  
    print(data)    

    # Save new post to the DB
    db.add(newPost)
    db.commit()

  except:
    # insert failed, so send error to front end
    print(sys.exc_info()[0])
    # insert failed, so rollback and send error to front end
    db.rollback()    
    return jsonify(message = 'Add post failed'), 500

 # session.clear()
 # session['user_id'] = newUser.id
 # session['loggedIn'] = True

  return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT'])
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    # retrieve post and update title property
    post = db.query(Post).filter(Post.id == id).one()
    post.title = data['title']
    db.commit()
  except:
    print(sys.exc_info()[0])
    db.rollback()
    return jsonify(message = 'Post not found'), 404
  return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
def delete(id):
  db = get_db()
  try:
    # delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()
  except:
    print(sys.exc_info()[0])
    db.rollback()
    return jsonify(message = 'Post not found'), 404
  return '', 204