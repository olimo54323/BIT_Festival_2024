from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from math import sqrt

from models import db
from models.user import User
from models.question import Question
from models.result import Result
from models.category import Category
from models.hobby import Hobby

app = Flask(__name__)

# Konfiguracja aplikacji
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mysql@localhost/bit'
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

# Mapa odpowiedzi na wartości punktowe
answer_values = {
    "zdecydowanie_tak": 2,
    "chyba_tak": 1,
    "nie_wiem": 0,
    "chyba_nie": -1,
    "zdecydowanie_nie": -2
}

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
        return redirect(url_for('index'))

    return render_template('signup.html')

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email']
        password = request.form['password']

        # Sprawdź, czy dane wejściowe to e-mail czy nazwa użytkownika
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

# Wylogowanie
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/about')  # Dodaj trasę /about
def about():
    return render_template('about.html')  # Tu wstaw ścieżkę do szablonu 'about.html'

@app.route('/categories')
def categories():
    categories = Category.query.all()  # Pobranie wszystkich kategorii z bazy danych
    return render_template('categories.html', categories=categories)


# Formularz z pytaniami (quiz)
@app.route('/quiz/<int:question_id>', methods=['GET', 'POST'])
@login_required
def single_question(question_id):
    """
    Wyświetla jedno pytanie quizu i obsługuje odpowiedzi.
    """
    questions = Question.query.all()
    question = Question.query.get_or_404(question_id)
    total_questions = len(questions)
    
    # Obsługa POST
    if request.method == 'POST':
        answer = request.form.get(f'question_{question_id}')
        if answer:
            # Zapisz odpowiedź w sesji
            if 'answers' not in session:
                session['answers'] = {}
            session['answers'][str(question_id)] = answer

            # Przejdź do następnego pytania, jeśli istnieje
            if question_id < total_questions:
                return redirect(url_for('single_question', question_id=question_id + 1))
            else:
                # Jeśli ostatnie pytanie, zakończ quiz
                return redirect(url_for('quiz_results'))
    
    # Pobierz odpowiedzi z sesji
    answers = session.get('answers', {})
    
    return render_template('quiz.html', question=question, question_id=question_id, total_questions=total_questions, answers=answers)


# Wyświetlenie wyników
@app.route('/result', methods=['GET', 'POST'])
@login_required
def quiz_results():
    """
    Zapisuje wyniki quizu i przekierowuje do strony wyników.
    """
    answers = session.get('answers', {})
    total_score_x = 0
    total_score_y = 0

    for question_id, answer in answers.items():
        question = Question.query.get(int(question_id))
        score = answer_values.get(answer, 0)
        if question.axis == 'X':
            total_score_x += score
        elif question.axis == 'Y':
            total_score_y += score

    # Zapisz wynik użytkownika w bazie danych
    result = Result(user_id=current_user.user_id, axis_x=total_score_x, axis_y=total_score_y)
    db.session.add(result)
    db.session.commit()

    # Wyczyść odpowiedzi z sesji
    session.pop('answers', None)
    
    return redirect(url_for('results'))

    

@app.route('/hobby/<name>')
def hobby_detail(name):
    """
    Wyświetla szczegóły wybranego hobby na podstawie jego nazwy.
    """
    # Wyszukiwanie hobby po nazwie (nazwa powinna być unikalna)
    hobby = Hobby.query.filter_by(hobby=name).first_or_404()
    return render_template('hobby.html', hobby=hobby)


# Funkcja wyszukiwania wektorowego
def vector_search(total_score_x, total_score_y, top_n=5):
    """
    Find hobbies closest to the given coordinates using Euclidean distance.
    """
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
    app.run(debug=True)
