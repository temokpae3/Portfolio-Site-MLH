import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import hashlib

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    database=os.getenv("MYSQL_DATABASE"),
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])

# Custom Jinja filter
def md5_hash(email):
    return hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest()

# Register the filter with Jinja
app.jinja_env.filters['md5'] = md5_hash

# Example data for display
work_experiences = [
    {
        "title": "Production Engineering Fellow",
        "company": "Major League Hacking",
        "location": "Remote",
        "duration": "June 2024 - Present",
    }
]

educations = [
    {
        "degree": "Master of Engineering in Computer Science",
        "university": "Virginia Tech",
        "location": "Falls Church, VA",
        "duration": "August 2024 - May 2026",
    },
    {
        "degree": "Bachelor of Science in Computer Science",
        "university": "State University of New York at Oswego",
        "location": "Oswego, NY",
        "duration": "January 2020 - May 2024",
        "description": "Graduated with Latin Honors Cum Laude. GPA: 3.34 GPA."
    }
]

hobbies = [
    {
        "name": "Hanging out with friends",
        "image_url": "./img/hobby1.jpg"
    },
    {
        "name": "Playing UNO",
        "image_url": "./img/hobby2.jpg"
    },
    {
        "name": "Going to broadway",
        "image_url": "./img/hobby3.jpg"
    },
    {
        "name": "Performing",
        "image_url": "./img/hobby4.jpg"
    }
]

@app.route("/")
def index():
    return render_template(
        "index.html",
        title="Temitope Emokpae",
        url=os.getenv("URL"),
    )

@app.route("/work", methods=["GET", "POST"])
def work():
    # This handles the POST requests to add a new work experience and education.
    # It extracts data from the form and appends it to the 'work_experiences' and 'educations' list.
    # Then, it redirects back to the index page after adding.
    if request.method == "POST":
        if "title" in request.form:
            new_experience = {
                "title": request.form["title"],
                "company": request.form["company"],
                "location": request.form["location"],
                "duration": request.form["duration"],
                "description": request.form["description"],
            }
            work_experiences.append(new_experience)
        elif "degree" in request.form:
            new_education = {
                "degree": request.form["degree"],
                "university": request.form["university"],
                "location": request.form["location"],
                "duration": request.form["duration"],
                "description": request.form["description"],
            }
            educations.append(new_education)
        return redirect(url_for("work"))

    return render_template(
        "work.html",
        title="Work and Education",
        work_experiences=work_experiences,
        educations=educations,
        url=os.getenv("URL"),
    )

@app.route('/hobbies', methods=['GET', 'POST'])
def hobbies_page():
    if request.method == 'POST':
        new_hobby = {
            "name": request.form["name"],
            "image_url": request.form["image_url"]
        }
        hobbies.append(new_hobby)
        return redirect(url_for('hobbies_page'))
    return render_template('hobbies.html', title="Hobbies", hobbies=hobbies, url=os.getenv("URL"))


@app.route('/places')
def places():
    return render_template('places.html', title="Cool Places I've Visited", url=os.getenv("URL"))

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts' : [
            model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_time_line_post(post_id):
    timeline_post = TimelinePost.get_by_id(post_id)
    timeline_post.delete_instance()
    return {
        'message': f'Timeline post with ID {post_id} deleted successfully.'
    }

@app.route('/timeline')
def timeline():
    timeline_posts = get_time_line_post()['timeline_posts']
    return render_template('timeline.html', title="Timeline", timeline_posts=timeline_posts)
