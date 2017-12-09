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

    def __init__(self, title, blog_body):
        self.title = title
        self.blog_body = blog_body
    
# Before request, set the allowed routes
@app.before_request
def blog_home():
    allowed_routes = ['blog','newpost']
    if request.endpoint not in allowed_routes:
        return redirect('/blog')

# Set the blog route
@app.route('/blog', methods=['POST','GET'])
def blog():
    if request.method == 'GET':
        id = request.args.get("id")                         # Get the id parameter
        blog_post = Blog.query.filter_by(id=id).all()       # Query by single post 
        posts = Blog.query.all()                            # Query all posts when form is rendered

        # Render the template and pass the parameters
        return render_template('blog.html',title="Build a Blog", blog_post=blog_post, posts=posts)

# Set the new post route
@app.route('/newpost', methods=['POST','GET'])
def newpost():

    # If the user enters values and attempts to submit validate the fields
    if request.method == 'POST':
        title = request.form['blog_title']
        title = title.strip()
        blog_body = request.form['blog_body']
        blog_body = blog_body.strip()

        # If either field is empty send a message to the user        
        if title == "" or blog_body == "" or len(title) < 1 or len(blog_body) < 1:
            if title == "" and blog_body == "":
                flash('The title is empty, please enter a title.','error')
                flash('The blog message is empty, please enter a message.','error')
                return render_template('newpost.html',blog_title=title,blog_body=blog_body)
            if title == "":
                flash('The title is empty, please enter a title.','error')
                return render_template('newpost.html',blog_title=title,blog_body=blog_body)
        if blog_body == "":
                flash('The blog message is empty, please enter a message.','error')
                return render_template('newpost.html',blog_title=title,blog_body=blog_body)
        else:
            # Submit users entry into the database
            new_blog_entry = Blog(title, blog_body)
            db.session.add(new_blog_entry)
            db.session.commit()
            blog_id = str(new_blog_entry.id)
            return redirect("/blog?id=" + blog_id)
    else:
        # If the method isn't post render the form
        return render_template('newpost.html')


# Set the home page route. In this application it's the blog page
@app.route('/',methods=['POST','GET'])
def index():

    # pocess the post method
    if request.method == 'POST':
        pass
    else:
        # Process get requests
        posts = Blog.query.all()                        # Query all blogs
        id = request.args.get("id")                     # Get the blog id
        blog_post = Blog.query.filter_by(id=id).all()   # Get an individual blog

        return render_template('blog.html',title="Build a Blog", blog_post=blog_post, posts=posts)

# If app is called from main run
if __name__ == '__main__':
    app.run()