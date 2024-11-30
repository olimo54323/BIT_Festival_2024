# main.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.user import User
from models.question import Question
from models.result import Result
from models.category import Category
from models.hobby import Hobby

app = Flask(__name__)

# Konfiguracja aplikacji
app.config['SECRET_KEY'] = 'your_secret_key'  # Ustaw swój klucz sekretu
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@localhost/bit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja bazy danych
db.init_app(app)

# Inicjalizacja LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Ładowanie użytkownika
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Strona główna
@app.route('/')
def index():
    return render_template("index.html")

# Rejestracja
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

        # Sprawdź, czy użytkownik już istnieje
        existing_user = User.query.filter((User.name == name) | (User.email == email)).first()
        if existing_user:
            flash('Użytkownik o takiej nazwie lub adresie e-mail już istnieje.')
            return redirect(url_for('signup'))

        # Hashowanie hasła
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Dodaj nowego użytkownika do bazy danych
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('quiz'))

    return render_template('signup.html')

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('quiz'))
        else:
            flash('Nieprawidłowa nazwa użytkownika lub hasło.')
            return redirect(url_for('login'))

    return render_template('login.html')

# Wylogowanie
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Mapa odpowiedzi na wartości punktowe
answer_values = {
    "zdecydowanie_tak": 2,
    "chyba_tak": 1,
    "nie_wiem": 0,
    "chyba_nie": -1,
    "zdecydowanie_nie": -2
}

# Formularz z pytaniami (quiz)
@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        total_score_x = 0
        total_score_y = 0
        answers = []
        questions = Question.query.all()
        for question in questions:
            answer = request.form.get(f'question_{question.question_id}')
            if answer:
                score = answer_values.get(answer, 0)
                if question.axis == 'X':
                    total_score_x += score
                elif question.axis == 'Y':
                    total_score_y += score
                answers.append({'question_id': question.question_id, 'score': score})
            else:
                answers.append({'question_id': question.question_id, 'score': 0})

        # Zapisz wynik użytkownika w bazie danych
        result = Result(user_id=current_user.user_id, axis_x=total_score_x, axis_y=total_score_y)
        db.session.add(result)
        db.session.commit()

        # Rekomendacja hobby na podstawie wyniku
        recommended_hobbies = recommend_hobby(total_score_x, total_score_y)

        return render_template('result.html', total_score_x=total_score_x, total_score_y=total_score_y, recommended_hobbies=recommended_hobbies)
    else:
        questions = Question.query.all()
        return render_template('quiz.html', questions=questions)

# Funkcja rekomendująca hobby
def recommend_hobby(total_score_x, total_score_y):
    # Mapowanie kategorii na wartości osi
    category_axis_values = {
        'Samodzielny i Artystyczny': {'x': -10, 'y': -10},
        'Samodzielny i Sportowy': {'x': -10, 'y': 10},
        'Grupowy i Artystyczny': {'x': 10, 'y': -10},
        'Grupowy i Sportowy': {'x': 10, 'y': 10}
    }

    hobbies = Hobby.query.join(Category).all()
    recommended = []

    for hobby in hobbies:
        category_name = hobby.category.category
        axis_values = category_axis_values.get(category_name)
        if axis_values:
            distance = ((axis_values['x'] - total_score_x) ** 2 + (axis_values['y'] - total_score_y) ** 2) ** 0.5
            recommended.append((distance, hobby.hobby))
    recommended.sort()
    top_hobbies = [name for _, name in recommended[:5]]
    return top_hobbies

if __name__ == '__main__':
    app.run(debug=True)
