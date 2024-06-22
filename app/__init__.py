import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Example data for display
work_experiences = []
educations = []
hobbies = []


@app.route("/")
def index():
    return render_template(
        "index.html",
        title="MLH Fellow",
        url=os.getenv("URL"),
        work_experiences=work_experiences,
        educations=educations,
        hobbies=hobbies,
    )


@app.route("/add_experience", methods=["POST"])
def add_experience():
    # This handles the POST requests to add a new work experience.
    # It extracts data from the form and appends it to the 'work_experiences' list.
    # Then, it redirects back to the index page after adding.
    new_experience = {
        "title": request.form["title"],
        "company": request.form["company"],
        "location": request.form["location"],
        "duration": request.form["duration"],
        "description": request.form["description"],
    }
    work_experiences.append(new_experience)
    return redirect(url_for("index"))


@app.route("/add_education", methods=["POST"])
def add_education():
    # This handles the POST requests to add more educations.
    # It extracts data from the form and appends it to the 'educations' list.
    # Then, it redirects back to the index page after adding.
    new_education = {
        "degree": request.form["degree"],
        "university": request.form["university"],
        "location": request.form["location"],
        "duration": request.form["duration"],
        "description": request.form["description"],
    }
    educations.append(new_education)
    return redirect(url_for("index"))


@app.route("/add_hobby", methods=["POST"])
def add_hobby():
    # This handles the POST requests to add a new hobby.
    # It extracts data from the form and appends it to the 'hobby' list.
    # Then, it redirects back to the index page after adding.
    new_hobby = {
        "name": request.form["name"],
        "description": request.form["description"],
    }
    hobbies.append(new_hobby)
    return redirect(url_for("index"))
