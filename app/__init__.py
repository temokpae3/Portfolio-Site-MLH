import os
import requests
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict
import hashlib

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        database=os.getenv("MYSQL_DATABASE"),
        port=3306
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
        "degree": "Master of Engineering in Computer Science and Application",
        "university": "Virginia Tech",
        "location": "Blacksburg, VA (D.C. Campus)",
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
    
    if not name or len(name) == 0:
        return render_template('400.html'), 400 
    
    email = request.form['email']
    if not '@' in email:
        return render_template('400.html', message="Invalid email"), 400
    
    content = request.form['content']
    if len(content) == 0:
        return render_template('400.html', message="Invalid content"), 400
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

@app.errorhandler(400)
def error_handler(*args):
    if not 'name' in request.values:
        return render_template('400.html', message="Invalid name"), 400
    
    if not 'content' in request.values == 0:
        return render_template('400.html', message="Invalid content"), 400
    
    if not 'email' in request.values:
        return render_template('400.html', message="Invalid email"), 400

    return render_template('400.html', message="Unknown Error Type"), 400

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health_check():
    statuses = []
    
    # Check the main application (self-check)
    try:
        mydb.connect(reuse_if_open=True)
        mydb.execute_sql('SELECT 1')
        statuses.append({'service': 'Database', 'status': 'Operational'})
    except Exception as e:
        statuses.append({'service': 'Database', 'status': f'Error: {str(e)}'})
    
    # Check the portfolio-site-mlh container
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            statuses.append({'service': 'Portfolio Site', 'status': 'Operational'})
        else:
            statuses.append({'service': 'Portfolio Site', 'status': 'Unhealthy'})
    except Exception as e:
        statuses.append({'service': 'Portfolio Site', 'status': f'Error: {str(e)}'})

    # Check the mysql container
    try:
        response = requests.get('http://localhost:3306/health')
        if response.status_code == 200:
            statuses.append({'service': 'MySQL', 'status': 'Operational'})
        else:
            statuses.append({'service': 'MySQL', 'status': 'Unhealthy'})
    except Exception as e:
        statuses.append({'service': 'MySQL', 'status': f'Error: {str(e)}'})

    # Check the nginx container
    try:
        response = requests.get('http://localhost:80/health')
        if response.status_code == 200:
            statuses.append({'service': 'Nginx', 'status': 'Operational'})
        else:
            statuses.append({'service': 'Nginx', 'status': 'Unhealthy'})
    except Exception as e:
        statuses.append({'service': 'Nginx', 'status': f'Error: {str(e)}'})

    # Render the health status in a template
    overall_status = all(service['status'] == 'Operational' for service in statuses)
    return render_template('health.html', status='Operational' if overall_status else 'Degraded', services=statuses)