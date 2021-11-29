import flask
import os
from flask_sqlalchemy import SQLAlchemy
from spotify import get_track_info
from genius import get_lyric

app = flask.Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://eepbivmxdbkgud:435f6b6200d40c405c1c7c2972535fbbc5c17add67ced8d23199e5ba2bbe5eb6@ec2-54-147-76-191.compute-1.amazonaws.com:5432/d9dia7409mhj5j"
# suppresses a warning - not strictly needed
app.config["SECRET_KEY"] = "the random string"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# define some Models!


class Todo_artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(120))


db.create_all()

# artist page


@app.route("/", methods=["GET", "POST"])  # Python decorator
def get_artist_id():
    todos_id = Todo_artist.query.all()
    artist_ids = []
    for todo_id in todos_id:
        artist_ids.append(todo_id.artist_id)
    if flask.request.method == "POST":
        artist_id = flask.request.form.get("artist_id")
        todo_id = Todo_artist(artist_id=artist_id)
        db.session.add(todo_id)
        db.session.commit()
        artist_ids.append(artist_id)
    return flask.render_template(
        "artist.html",
        artist_ids=artist_ids,
    )


# index page and saving to database
@app.route("/index", methods=["GET", "POST"])  # Python decorator
def index():
    save_artist = Todo_artist.query.all()
    artist_id = []

    for i in save_artist:
        artist_id.append(i.artist_id)
    if flask.request.method == "POST":
        artist_id = flask.request.form.get("artist_id")
        for i in artist_id:
            if artist_id == i:
                flask.flash("id exists. login in instead")
                return flask.redirect("/index")
    i = Todo_artist(artist_id=artist_id)
    db.session.add(i)
    db.session.commit()

    data = get_track_info(artist_id)
    lyrics_url = get_lyric(data["artists"])

    return flask.render_template(
        "index.html",
        artists=data["artists"],
        name=data["name"],
        preview_url=data["preview_url"],
        image=data["image"],
        lyrics_url=lyrics_url,
    )


app.run(debug=True)
