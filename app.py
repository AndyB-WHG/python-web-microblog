import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))

    

    app.db = client.microblog

    @app.route("/", methods = ["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")   
            """ get("content") is used because 'content' is the 'name' 
                we gave the input field in 'home.html' """
            formatted_date = datetime.datetime.today().strftime("%d-%m-%Y")
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"], 
                entry["date"], 
                datetime.datetime.strptime(entry["date"], "%d-%m-%Y").strftime("%d %b")
            )
            for entry in app.db.entries.find({})
        ]

        return render_template("home.html", entries=entries_with_date)
    
    return app