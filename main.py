import os
from wtforms import StringField, SubmitField, URLField, SelectField
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
FLASK_RUN_PORT = 5008

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

with app.app_context():
    db.create_all()

class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = URLField('Map_url', validators=[DataRequired()])
    img_url = URLField('Img_url', validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    seats = StringField("Seats", validators=[DataRequired()])
    has_toilet = StringField("has_toilet", validators=[DataRequired()])
    has_wifi = StringField("has_wifi", validators=[DataRequired()])
    has_sockets = StringField("has_sockets", validators=[DataRequired()])
    can_take_calls = StringField("can_take_calls", validators=[DataRequired()])
    coffee_price = StringField("coffee_price", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_post = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            seats=request.form.get("seats"),
            has_toilet=bool(request.form.get("has_toilet")),
            has_wifi=bool(request.form.get("has_wifi")),
            has_sockets=bool(request.form.get("has_sockets")),
            can_take_calls=bool(request.form.get("can_take_calls")),
            coffee_price=request.form.get("coffee_price"),
        )
        with app.app_context():
            db.session.add(new_post)
            db.session.commit()
        return redirect(url_for('get_all_posts')) #redirect(url_for('cafes')) #cafes()
    return render_template('add.html', form=form, post="New Post")


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = Cafe.query.get(post_id)
    return render_template("post.html", post=requested_post)


@app.route('/cafes')
def get_all_posts():
    posts = Cafe.query.all()
    return render_template("cafes.html", all_posts=posts)

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post_id = post_id
    requested_post = Cafe.query.get(post_id)
    edit_form = CafeForm(
        name=requested_post.name,
        map_url=requested_post.map_url,
        img_url=requested_post.img_url,
        location=requested_post.location,
        seats=requested_post.seats,
        has_toilet=int(requested_post.has_toilet),
        has_wifi=int(requested_post.has_wifi),
        has_sockets=int(requested_post.has_sockets),
        can_take_calls=int(requested_post.can_take_calls),
        coffee_price=requested_post.coffee_price,
    )
    if edit_form.validate_on_submit():
        requested_post.name = request.form.get("name")
        requested_post.map_url = request.form.get("map_url")
        requested_post.img_url = request.form.get("img_url")
        requested_post.location = request.form.get("location")
        requested_post.seats = request.form.get("seats")
        requested_post.has_toilet = bool(request.form.get("has_toilet"))
        requested_post.has_wifi = bool(request.form.get("has_wifi"))
        requested_post.has_sockets = bool(request.form.get("has_sockets"))
        requested_post.can_take_calls = bool(request.form.get("can_take_calls"))
        requested_post.coffee_price = request.form.get("coffee_price")
        db.session.commit()
        return render_template("post.html", post=requested_post)
    return render_template("make-post.html", form=edit_form, post="Edit Post")

@app.route("/delete/<int:post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    post_id = post_id
    deleted_post = Cafe.query.get(post_id)
    db.session.delete(deleted_post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4444)