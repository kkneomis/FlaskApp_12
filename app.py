from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template("index.html",
                           posts=posts,
                           categories=categories)

tags = db.Table('tags',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))

    tags = db.relationship('Category', secondary=tags,
                           backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Post %r>' % self.content


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


@app.route('/addcategory', methods=['POST', 'GET'])
def addcategory():
    name = request.form['name']
    category = Category(name)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/addpost', methods=['POST', 'GET'])
def addpost():
    content = request.form['content']
    post = Post(content)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/addtags', methods=['POST', 'GET'])
def addtags():
    tags = request.form.getlist('tags')
    print tags
    post_id = request.form['post']
    post = db.session.query(Post).get(post_id)
    for tag in tags:
        category = db.session.query(Category).get(tag)
        post.tags.append(category)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run()
