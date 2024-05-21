from flask import Flask, render_template, request, session
import random
import string
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'eternal'
app.secret_key = "your_secret_key"

mysql = MySQL(app)

# Dictionary to store room IDs for each session
session_rooms = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create_room", methods=["GET", "POST"])
def create_room():
    if "room_id" in session and session["room_id"] in session_rooms:
        created_room = True
        question = session_rooms[session["room_id"]]["question"]
        answer = session_rooms[session["room_id"]]["answer"]
    else:
        question = retrieveQuestion()  
        room_id = generateRoomID()
        session["room_id"] = room_id  
        answer = None  
        session_rooms[session["room_id"]] = {"question": question, "answer": answer}
        created_room = False

    success_message = None

    if request.method == "POST":
        answer = request.form.get("answer")
        saveVariables(answer, question[0])
        session_rooms[session["room_id"]]["answer"] = answer
        success_message = "Thank you! Now wait for your partner's answer."

    return render_template("create_room.html", created_room=created_room, question=question[1], answer=answer, success_message=success_message, room_id=session["room_id"])

def saveVariables(answer, question_id):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO rooms (roomid, questionid, answer1, answer2) VALUES (%s, %s, %s, %s)", 
                   (session["room_id"], question_id, answer, None))
    mysql.connection.commit()
    cursor.close()

def retrieveQuestion():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT questionid, questiontext FROM questions ORDER BY RAND() LIMIT 1")
    question = cursor.fetchone()
    cursor.close()
    return question

def generateRoomID():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route("/join_room", methods=["GET"])
def join_room():
    return render_template("newSession.html")

if __name__ == "__main__":
    app.run(debug=True)
