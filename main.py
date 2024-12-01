from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from math import sqrt
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

from models import db
from models.user import User
from models.question import Question
from models.result import Result
from models.category import Category
from models.hobby import Hobby
from models.chatroom import ChatRoom
from models.chatroom import Message

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mysql@localhost/bit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

answer_values = {
    "zdecydowanie_tak": 2,
    "chyba_tak": 1,
    "nie_wiem": 0,
    "chyba_nie": -1,
    "zdecydowanie_nie": -2
}

# Routes remain the same until chat functionality
@app.route('/')
def index():
    recommended_hobbies = []
    if current_user.is_authenticated:
        # Check if the user has taken the quiz
        result = Result.query.filter_by(user_id=current_user.user_id).order_by(Result.result_id.desc()).first()
        if result:
            # Get recommended hobbies based on the latest quiz result
            recommended_hobbies = vector_search(result.axis_x, result.axis_y, top_n=5)
    
    return render_template("index.html", recommended_hobbies=recommended_hobbies)

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('Hasła nie są takie same.')
            return redirect(url_for('signup'))

        existing_user = User.query.filter((User.name == name) | (User.email == email)).first()
        if existing_user:
            flash('Użytkownik o takiej nazwie lub adresie e-mail już istnieje.')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('index'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        user = User.query.filter(
            (User.name == username_or_email) | (User.email == username_or_email)
        ).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Nieprawidłowa nazwa użytkownika/adres e-mail lub hasło.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


# Formularz z pytaniami (quiz)
@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'])
@login_required
def single_question(question_id):
    """
    Displays one quiz question and handles answers.
    """
    questions = Question.query.all()
    question = Question.query.get_or_404(question_id)
    total_questions = len(questions)

    if request.method == 'POST':
        answer = request.form.get(f'question_{question_id}')
        if answer:
            # Initialize answers dictionary if it doesn't exist
            if 'answers' not in session:
                session['answers'] = {}
            
            # Save the answer and calculate its score
            session['answers'][str(question_id)] = {
                'answer': answer,
                'axis': question.axis,
                'score': answer_values[answer]
            }
            
            # Make sure to mark session as modified
            session.modified = True

            if question_id < total_questions:
                return redirect(url_for('single_question', question_id=question_id + 1))
            else:
                return redirect(url_for('index'))

    return render_template('quiz.html', 
                         question=question, 
                         question_id=question_id, 
                         total_questions=total_questions, 
                         answers=session.get('answers', {}))

@app.route('/result', methods=['GET', 'POST'])
@login_required
def quiz_results():
    """
    Calculates final scores and saves quiz results.
    """
    answers = session.get('answers', {})
    
    # Initialize scores
    total_score_x = 0
    total_score_y = 0
    
    # Calculate scores for all answers
    for question_id, answer_data in answers.items():
        score = answer_data['score']
        axis = answer_data['axis']
        
        if axis == 'X':
            total_score_x += score
        elif axis == 'Y':
            total_score_y += score
    
    # Debug output
    print(f"Answers data: {answers}")
    print(f"Final scores - X: {total_score_x}, Y: {total_score_y}")
    
    # Save result to database
    result = Result(
        user_id=current_user.user_id,
        axis_x=total_score_x,
        axis_y=total_score_y
    )
    db.session.add(result)
    db.session.commit()

    # Clear the session answers
    session.pop('answers', None)

    return redirect(url_for('results'))

@app.route('/results')
@login_required
def results():
    """
    Displays user results and recommended hobbies.
    """
    result = Result.query.filter_by(user_id=current_user.user_id).order_by(Result.result_id.desc()).first()
    if result:
        recommended_hobbies = vector_search(result.axis_x, result.axis_y, top_n=5)
        return render_template('result.html', result=result, recommended_hobbies=recommended_hobbies)
    else:
        flash('No results found. Please take the quiz.')
        return redirect(url_for('single_question', question_id=1))



@app.route('/hobby/<name>')
def hobby_detail(name):
    """
    Wyświetla szczegóły wybranego hobby na podstawie jego nazwy.
    """
    hobby = Hobby.query.filter_by(hobby=name).first_or_404()
    return render_template('hobby.html', hobby=hobby)

# Modified chat functionality - removed room creation
@app.route('/chat')
@login_required
def chat_rooms():
    rooms = ChatRoom.query.all()
    return render_template('chat/rooms.html', rooms=rooms)

@app.route('/chat/<int:room_id>')
@login_required
def chat_room(room_id):
    room = ChatRoom.query.get_or_404(room_id)
    if current_user not in room.participants:
        room.participants.append(current_user)
        db.session.commit()
    messages = Message.query.filter_by(room_id=room_id).order_by(Message.timestamp).all()
    return render_template('chat/room.html', room=room, messages=messages)

# SocketIO event handlers
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{current_user.name} has joined the room.'}, room=room)

@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'{current_user.name} has left the room.'}, room=room)

@socketio.on('message')
def handle_message(data):
    room_id = data['room']
    content = data['message']
    
    # Create and save new message
    new_message = Message(
        content=content,
        room_id=room_id,
        user_id=current_user.user_id
    )
    db.session.add(new_message)
    db.session.commit()
    
    # Emit the message to all users in the room
    emit('message', {
        'user': current_user.name,
        'message': content,
        'timestamp': datetime.utcnow().strftime('%H:%M')
    }, room=room_id)

def vector_search(total_score_x, total_score_y, top_n=5):
    hobbies = Hobby.query.all()
    results = []

    for hobby in hobbies:
        distance = sqrt((hobby.axis_x - total_score_x) ** 2 + 
                        (hobby.axis_y - total_score_y) ** 2)
        results.append({
            "hobby": hobby.hobby,
            "hobby_id": hobby.hobby_id,
            "description": hobby.description,
            "distance": distance
        })

    results.sort(key=lambda x: x["distance"])
    return results[:top_n]



if __name__ == '__main__':
    socketio.run(app, debug=True)