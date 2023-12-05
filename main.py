####Tutorial from @codewithharry Akamai Developers, https://youtu.be/NDYhGH586w4
#pip install flask and flas_sqlalchemy just as they're called here
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
#db = SQLAlchemy()
#db.init_app(app)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False) #nullable=False not doing anything here
    topicId = db.Column(db.String)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        topic = Topic(
            title = request.form["title"],
            description = request.form["description"]
            )
        db.session.add(topic)
        db.session.commit()

    topics = db.session.execute(db.select(Topic)).scalars()
    return render_template("/index.html", topics=topics)

@app.route("/topic/<int:id>", methods=["GET","POST"])
def topic(id):
    if request.method == "POST":
        comment = Comment(
            text = request.form["comment"],
            topicId = id
            )
        db.session.add(comment)
        db.session.commit()
    topic = db.get_or_404(Topic, id)
    #getting error now object of type query has no len()
#            <!-- query no len() error but he doesnt get this error <h6 class="border-bottom pb-2 mb-0">Comments ({{comments|length}})</h6> -->
    comments = Comment.query.filter_by(topicId=id) #filter_by in flask sqlalchemy, where in regular sqlalchemy
    return render_template("topic.html", topic=topic, comments=comments)

app.run(debug=True, port=5001)