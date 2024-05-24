from flask import Flask, render_template, request, session, redirect, url_for, flash
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

session_rooms = {}


#ROUTING 


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
    if request.method == "POST":
        answer = request.form.get("answer")
        saveVariables(answer, question[0])
        session_rooms[session["room_id"]]["answer"] = answer
    return render_template("create_room.html", created_room=created_room, question=question[1], answer=answer, room_id=session["room_id"])



# ^ WORKS DON'T CHANGE 
@app.route("/join_room", methods=["GET", "POST"])
def join_room():
    if request.method == "GET":
        room_id = request.args.get("oldID")
        if room_id and checkRoomID(room_id):
            question = retrieveQuestionByRoomID(room_id)
            return render_template("join_room.html", question=question, room_id=room_id, submitted=False)
        else:
            flash("Room ID not found. Please try again.")
            return redirect(url_for("home"))

@app.route("/submit_answer/<room_id>", methods=["POST"])
def submit_answer(room_id):
    answer = request.form.get("answer")
    saveAnswer(room_id, answer)
    partner_answer = getPartnerAnswer(room_id)
    question = retrieveQuestionByRoomID(room_id)

    flash("Thank you! Your answer has been submitted.")
    return render_template("join_room.html", question=question, room_id=room_id, answer=answer, partner_answer=partner_answer, submitted=True)



# FUNCTIONS 

def getPartnerAnswer(room_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT answer1 FROM rooms WHERE roomid = %s", (room_id,))
    answers = cursor.fetchone()
    cursor.close()
    return answers[0]


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

def checkRoomID(room_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM rooms WHERE roomid = %s", (room_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

def retrieveQuestionByRoomID(room_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT q.questiontext FROM rooms r JOIN questions q ON r.questionid = q.questionid WHERE r.roomid = %s", (room_id,))
    question = cursor.fetchone()[0]
    cursor.close()
    return question

def saveAnswer(room_id, answer):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE rooms SET answer2 = %s WHERE roomid = %s", (answer, room_id))
    mysql.connection.commit()
    cursor.close()


if __name__ == "__main__":
    app.run(debug=True)
