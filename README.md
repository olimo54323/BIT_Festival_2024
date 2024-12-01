# BIT Festival 2024 - Platforma Rekomendacji Hobby

## Przegląd
Aplikacja internetowa zbudowana przy użyciu Flask, która pomaga użytkownikom odkrywać nowe hobby na podstawie ich preferencji poprzez interaktywny system quizów. Platforma oferuje również pokoje czatu w czasie rzeczywistym, gdzie użytkownicy mogą dyskutować o swoich zainteresowaniach.

## Funkcjonalności
- **Uwierzytelnianie Użytkowników**
  - Rejestracja i logowanie
  - Bezpieczne hashowanie haseł
  - Zarządzanie sesjami użytkowników

- **Interaktywny System Quizów**
  - Dynamiczny kwestionariusz z pytaniami wielokrotnego wyboru
  - System punktacji dwuosiowej (współrzędne X i Y)
  - Śledzenie postępu przez pytania

- **Rekomendacje Hobby**
  - Algorytm dopasowywania hobby oparty na wektorach
  - Spersonalizowane rekomendacje na podstawie wyników quizu
  - Szczegółowe opisy i informacje o hobby

- **System Czatu w Czasie Rzeczywistym**
  - Wiele pokojów czatu dla różnych tematów
  - Komunikacja w czasie rzeczywistym przy użyciu SocketIO
  - Wskaźniki obecności użytkowników
  - Historia wiadomości

## Technologie
- **Backend**: Python Flask
- **Baza danych**: MySQL
- **ORM**: SQLAlchemy
- **Uwierzytelnianie**: Flask-Login
- **Komunikacja w czasie rzeczywistym**: Flask-SocketIO
- **Frontend**: HTML, CSS, JavaScript
- **Bezpieczeństwo**: Funkcje bezpieczeństwa Werkzeug

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/olimo54323/BIT_Festival_2024.git
cd BIT_Festival_2024
```

2. Utwórz i aktywuj środowisko wirtualne:
```bash
python -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate
```

3. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```

4. Skonfiguruj bazę danych MySQL:
- Utwórz nową bazę danych o nazwie 'bit'
- Zaktualizuj ciąg połączenia z bazą danych w `main.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mysql@localhost/bit'
```

5. Zainicjalizuj bazę danych:
```bash
flask db upgrade
```

## Uruchamianie Aplikacji

1. Uruchom serwer deweloperski:
```bash
python main.py
```

2. Dostęp do aplikacji pod adresem `http://localhost:5000`

## Struktura Projektu
```
BIT_Festival_2024/
├── main.py                 # Punkt wejścia aplikacji
├── models/                 # Modele bazy danych
│   ├── __init__.py
│   ├── user.py
│   ├── question.py
│   ├── result.py
│   ├── category.py
│   ├── hobby.py
│   ├── chatroom.py
├── templates/             # Szablony HTML
│   ├── base.html
│   ├── index.html
│   ├── quiz.html
│   ├── result.html
│   └── chat/
│       ├── rooms.html
│       └── room.html
└── static/               # Pliki statyczne (CSS, JS, obrazy)
```

## Jak Przyczynić się do Rozwoju
1. Zrób fork repozytorium
2. Utwórz nową gałąź (`git checkout -b funkcjonalnosc/ulepszenie`)
3. Wprowadź swoje zmiany
4. Zatwierdź zmiany (`git commit -am 'Dodaj nową funkcjonalność'`)
5. Wypchnij do gałęzi (`git push origin funkcjonalnosc/ulepszenie`)
6. Utwórz Pull Request

## Licencja
Ten projekt jest open source i dostępny na [Licencji MIT](LICENSE).

## Kontakt
- GitHub: [@olimo54323](https://github.com/olimo54323)

## Podziękowania
- Stworzono na BIT Festival 2024
- Podziękowania dla wszystkich współtwórców i uczestników