from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Article %r>" % self.id


@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    context = {"articles": articles}
    return render_template("posts.html", **context)


@app.route("/posts/<int:id>")
def post(id):
    article = Article.query.get(id)
    context = {"article": article}
    return render_template("post.html", **context)


@app.route("/posts/create", methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        article = Article(title=title, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect(url_for("posts"))
        except:
            return render_template("create_article.html")
    else:
        return render_template("create_article.html")


@app.route("/posts/<int:id>/delete")
def delete_article(id):
    article = Article.query.get(id)
    try:
        db.session.delete(article)
        db.session.commit()
    except:
        context = {"article": article}
        return render_template("post.html", **context)
    return redirect(url_for("posts"))


@app.route("/posts/<int:id>/redact", methods=["POST", "GET"])
def redact_article(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form["title"]
        article.text = request.form["text"]
        try:
            db.session.commit()
            context = {"id": id}
            return redirect(url_for("post", **context))
        except:
            return render_template("posts.html")
    else:
        context = {"article": article}
        return render_template("redact_article.html", **context)


if __name__ == "__main__":
    app.run(debug=True)
