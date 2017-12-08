from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import Column, Integer, String, Boolean
#from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:sleepy@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'yfdn3656ymcjz&vzAIP'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    blog_body = db.Column(db.String(2500))
    #owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, blog_body):
        self.title = title
        self.blog_body = blog_body
#       self.owner = owner
    
"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    tasks = db.relationship('Task', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password
"""

@app.before_request
def blog_home():
    allowed_routes = ['blog']
    if request.endpoint not in allowed_routes:
        return redirect('/blog')


@app.route('/blog', methods=['POST','GET'])
def blog():
    posts = Blog.query.all()
    return render_template('blog.html',title="Build a Blog", posts=posts)
     
@app.route('/newpost', methods=['POST'])
def newpost():
    return render_template('newpost.html',title="Add a Blog Entry")


@app.route('/',methods=['POST','GET'])
def index():

    posts = Blog.query.all()
    if request.method == 'POST':
        posts = Blog.query.all()
 #      new_post = Blog.query.filter_by(id=d)        
    else:
#       posts = Blog.query.all()
        return redirect('/blog?id=' + post.id)
        new_post = Blog.query.filter_by(id=d)        
#    owner = User.query.filter_by(email=session['email']).first()
#    if request.method == 'POST':
#        task_name = request.form['task']
#        new_task = Task(task_name, owner)
#        db.session.add(new_task)
#        db.session.commit()

#   tasks = Task.query.all()
#    tasks = Task.query.filter_by(completed=False,owner=owner).all()
#    completed_tasks = Task.query.filter_by(completed=True,owner=owner).all()

 #       tasks.append(task)
    
    return render_template('blog.html',title="Build a Blog", posts=posts,id=id)

    


if __name__ == '__main__':
    app.run()