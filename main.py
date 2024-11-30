from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Konfiguracja aplikacji
app.config['SECRET_KEY'] = 'your_secret_key'  # Ustaw swój klucz sekretu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicjalizacja bazy danych
db = SQLAlchemy(app)

# Inicjalizacja LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Model użytkownika
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

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
        username = request.form['username']
        password = request.form['password']

        # Sprawdź, czy użytkownik już istnieje
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Użytkownik o takiej nazwie już istnieje.')
            return redirect(url_for('signup'))

        # Hashowanie hasła
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Dodaj nowego użytkownika do bazy danych
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('quiz'))

    return render_template('signup.html')

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
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

# Lista pytań (40 pytań z przypisaniem do osi)
questions = [
    {"text": "Czy wolisz spędzać czas wolny samotnie czy w towarzystwie innych?", "axis": "X"},
    {"text": "Czy preferujesz pracę nad projektami samemu czy w zespole?", "axis": "X"},
    {"text": "Czy czerpiesz więcej radości z aktywności indywidualnych czy grupowych?", "axis": "X"},
    {"text": "Czy wolisz tworzyć sztukę czy uprawiać sport?", "axis": "Y"},
    {"text": "Czy interesują Cię zajęcia artystyczne czy sportowe?", "axis": "Y"},
    {"text": "Czy wolisz ćwiczyć samodzielnie czy z partnerem/trenerem?", "axis": "X"},
    {"text": "Czy lubisz uczestniczyć w wydarzeniach kulturalnych czy sportowych?", "axis": "Y"},
    {"text": "Czy preferujesz czytanie książek czy granie w gry zespołowe?", "axis": "X"},
    {"text": "Czy czerpiesz więcej satysfakcji z malowania czy z gry w piłkę nożną?", "axis": "Y"},
    {"text": "Czy wolisz zajęcia wymagające kreatywności czy fizycznej aktywności?", "axis": "Y"},
    {"text": "Czy preferujesz indywidualne lekcje czy zajęcia grupowe?", "axis": "X"},
    {"text": "Czy wolisz planować swoje działania samodzielnie czy zgodnie z planem grupy?", "axis": "X"},
    {"text": "Czy czerpiesz przyjemność z pisania czy z rywalizacji sportowej?", "axis": "Y"},
    {"text": "Czy wolisz słuchać muzyki czy kibicować drużynie sportowej?", "axis": "Y"},
    {"text": "Czy preferujesz zwiedzanie galerii sztuki czy uczestnictwo w meczach sportowych?", "axis": "Y"},
    {"text": "Czy lubisz medytację czy ćwiczenia w grupie?", "axis": "X"},
    {"text": "Czy wolisz grać na instrumencie czy uprawiać sport zespołowy?", "axis": "Y"},
    {"text": "Czy czerpiesz radość z fotografowania czy z biegania w maratonach?", "axis": "Y"},
    {"text": "Czy wolisz spędzać czas na majsterkowaniu czy na treningach drużynowych?", "axis": "X"},
    {"text": "Czy interesuje Cię taniec solowy czy taniec w grupie?", "axis": "X"},
    {"text": "Czy preferujesz samotne wędrówki czy zorganizowane wycieczki?", "axis": "X"},
    {"text": "Czy wolisz tworzyć rękodzieło czy uczestniczyć w sportach ekstremalnych?", "axis": "Y"},
    {"text": "Czy czerpiesz więcej satysfakcji z ogrodnictwa czy z treningów na siłowni?", "axis": "Y"},
    {"text": "Czy wolisz naukę programowania czy gry zespołowe online?", "axis": "X"},
    {"text": "Czy preferujesz gry planszowe czy gry zespołowe?", "axis": "X"},
    {"text": "Czy lubisz uczyć się nowych technik artystycznych czy sportowych?", "axis": "Y"},
    {"text": "Czy wolisz zajęcia kulinarne czy sporty wodne?", "axis": "Y"},
    {"text": "Czy czerpiesz przyjemność z układania puzzli czy z gier sportowych?", "axis": "Y"},
    {"text": "Czy preferujesz obserwację przyrody czy wspinaczkę z przyjaciółmi?", "axis": "X"},
    {"text": "Czy wolisz indywidualne zajęcia fitness czy zajęcia fitness w grupie?", "axis": "X"},
    {"text": "Czy interesuje Cię kaligrafia czy sztuki walki?", "axis": "Y"},
    {"text": "Czy wolisz pisanie poezji czy taniec towarzyski?", "axis": "Y"},
    {"text": "Czy czerpiesz radość z projektowania graficznego czy z jazdy na rowerze w grupie?", "axis": "Y"},
    {"text": "Czy preferujesz samotne zwiedzanie muzeów czy grupowe wycieczki sportowe?", "axis": "X"},
    {"text": "Czy wolisz czytać literaturę piękną czy magazyny sportowe?", "axis": "Y"},
    {"text": "Czy lubisz pracować nad projektami DIY czy uczestniczyć w drużynowych grach planszowych?", "axis": "X"},
    {"text": "Czy wolisz uczyć się języków obcych czy grać w siatkówkę?", "axis": "Y"},
    {"text": "Czy czerpiesz więcej radości z pisania kodu czy z uprawiania sportów drużynowych?", "axis": "X"},
    {"text": "Czy preferujesz samotne ćwiczenia jogi czy zajęcia aerobiku w grupie?", "axis": "X"},
    {"text": "Czy wolisz udział w konkursach literackich czy sportowych?", "axis": "Y"}
]

# Mapa odpowiedzi na wartości punktowe
answer_values = {
    "zdecydowanie_tak": 2,
    "chyba_tak": 1,
    "nie_wiem": 0,
    "chyba_nie": -1,
    "zdecydowanie_nie": -2
}

# Formularz z pytaniami (zabezpieczony logowaniem)
@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        total_score_x = 0
        total_score_y = 0
        answers = []
        for i, question in enumerate(questions):
            answer = request.form.get(f'question_{i}')
            if answer:
                score = answer_values.get(answer, 0)
                if question['axis'] == 'X':
                    total_score_x += score
                elif question['axis'] == 'Y':
                    total_score_y += score
                answers.append(score)
            else:
                answers.append(0)

        # Rekomendacja hobby
        recommended_hobbies = recommend_hobby(total_score_x, total_score_y)

        return render_template('result.html', total_score_x=total_score_x, total_score_y=total_score_y, recommended_hobbies=recommended_hobbies)
    return render_template('quiz.html', questions=enumerate(questions))

# Lista hobby z przypisanymi współrzędnymi
hobby_data = [
    # Samodzielny i Artystyczny
    {"name": "Pisanie", "x": -10, "y": -10},
    {"name": "Fotografia", "x": -9, "y": -9},
    {"name": "Malowanie", "x": -8, "y": -10},
    {"name": "Rysunek", "x": -7, "y": -9},
    {"name": "Rzeźbiarstwo", "x": -6, "y": -10},
    {"name": "Gra na instrumencie muzycznym", "x": -5, "y": -9},
    {"name": "Projektowanie graficzne", "x": -4, "y": -10},
    {"name": "Tworzenie biżuterii", "x": -3, "y": -9},
    {"name": "Modelarstwo", "x": -2, "y": -10},
    {"name": "Kaligrafia", "x": -1, "y": -9},
    {"name": "Edycja wideo", "x": -2, "y": -8},
    {"name": "Pisanie poezji", "x": -3, "y": -8},
    {"name": "Programowanie", "x": -4, "y": -7},
    {"name": "Astrofotografia", "x": -5, "y": -8},
    {"name": "Origami", "x": -6, "y": -7},

    # Samodzielny i Sportowy
    {"name": "Bieganie", "x": -10, "y": 10},
    {"name": "Pływanie", "x": -9, "y": 9},
    {"name": "Jazda na rowerze", "x": -8, "y": 10},
    {"name": "Joga", "x": -7, "y": 9},
    {"name": "Wspinaczka górska", "x": -6, "y": 10},
    {"name": "Sztuki walki", "x": -5, "y": 9},
    {"name": "Narciarstwo", "x": -4, "y": 10},
    {"name": "Łucznictwo", "x": -3, "y": 9},
    {"name": "Golf", "x": -2, "y": 10},
    {"name": "Surfing", "x": -1, "y": 9},
    {"name": "Kajakarstwo", "x": -2, "y": 8},
    {"name": "Łyżwiarstwo", "x": -3, "y": 8},
    {"name": "Nordic walking", "x": -4, "y": 7},
    {"name": "Tai chi", "x": -5, "y": 8},
    {"name": "Ćwiczenia na siłowni", "x": -6, "y": 7},

    # Grupowy i Artystyczny
    {"name": "Teatr amatorski", "x": 10, "y": -10},
    {"name": "Chór", "x": 9, "y": -9},
    {"name": "Zespół muzyczny", "x": 8, "y": -10},
    {"name": "Taniec towarzyski", "x": 7, "y": -9},
    {"name": "Warsztaty kulinarne", "x": 6, "y": -10},
    {"name": "Fotografia plenerowa w grupie", "x": 5, "y": -9},
    {"name": "Klub książki", "x": 4, "y": -10},
    {"name": "Klub filmowy", "x": 3, "y": -9},
    {"name": "Grupowe zajęcia plastyczne", "x": 2, "y": -10},
    {"name": "Improwizacja komediowa", "x": 1, "y": -9},
    {"name": "Orkiestra", "x": 2, "y": -8},
    {"name": "Zajęcia z ceramiki", "x": 3, "y": -8},
    {"name": "Projektowanie mody", "x": 4, "y": -7},
    {"name": "Grupowe warsztaty teatralne", "x": 5, "y": -8},
    {"name": "Flash mob", "x": 6, "y": -7},

    # Grupowy i Sportowy
    {"name": "Piłka nożna", "x": 10, "y": 10},
    {"name": "Koszykówka", "x": 9, "y": 9},
    {"name": "Siatkówka", "x": 8, "y": 10},
    {"name": "Rugby", "x": 7, "y": 9},
    {"name": "Hokej", "x": 6, "y": 10},
    {"name": "Baseball", "x": 5, "y": 9},
    {"name": "Piłka ręczna", "x": 4, "y": 10},
    {"name": "Wioślarstwo", "x": 3, "y": 9},
    {"name": "Żeglarstwo", "x": 2, "y": 10},
    {"name": "Paintball", "x": 1, "y": 9},
    {"name": "Krykiet", "x": 2, "y": 8},
    {"name": "Futbol amerykański", "x": 3, "y": 8},
    {"name": "Grupowe biegi na orientację", "x": 4, "y": 7},
    {"name": "Aerobik w grupie", "x": 5, "y": 8},
    {"name": "Zumba", "x": 6, "y": 7}
]

def recommend_hobby(total_score_x, total_score_y):
    distances = []
    for hobby in hobby_data:
        distance = ((hobby['x'] - total_score_x) ** 2 + (hobby['y'] - total_score_y) ** 2) ** 0.5
        distances.append((distance, hobby['name']))
    distances.sort()
    top_hobbies = [name for _, name in distances[:5]]
    return top_hobbies

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzenie tabel w bazie danych
    app.run(debug=True)
