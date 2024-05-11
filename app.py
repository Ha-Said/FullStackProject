from flask import Flask, redirect, url_for, render_template, request, session, flash
import random
import string

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for session encryption

# Dictionary to store room IDs for each session
session_rooms = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create_room", methods=["GET", "POST"])
def create_room():
    if "room_id" in session:
        # If room ID already exists in the session, set created_room to True
        # and pass question and answer to the template
        created_room = True
        question = session_rooms[session["room_id"]]["question"]
        answer = session_rooms[session["room_id"]]["answer"]
        return render_template("create_room", created_room=created_room, question=question, answer=answer)
    else:
        # Generate a new question and room ID
        question = retrieveQuestion()  
        room_id = generateRoomID()
        # Store the question and room ID

        session["room_id"] = room_id  
        answer = None  
        session_rooms[session["room_id"]] = {"question": question, "answer": answer}
        created_room = False
        if request.method == "POST":
            # If it's a POST request, store the user's answer
            answer = request.form.get("answer")
            saveVariables(answer,question[0]) 
        return render_template("create_room.html", created_room=created_room, question=question[1], answer=answer)
        

@app.route("/join_room", methods=["GET"])
def join_room():
    return render_template("newSession.html")







