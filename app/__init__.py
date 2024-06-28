import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

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

