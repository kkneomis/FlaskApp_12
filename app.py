from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flaskr.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship("Category", back_populates="post")

    def __init__(self, content, category):
        self.content = content
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.content


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    post = relationship("Post", uselist=False, back_populates="category")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


@app.route('/addpost', methods=['POST', 'GET'])
def add():
    content = request.form['content']
    category = Category(request.form['category'])
    post = Post(content, category)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run()
