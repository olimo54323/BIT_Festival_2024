-- @block
CREATE TABLE users(
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255)NOT NULL UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN
);

-- @block
CREATE TABLE questions(
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    question VARCHAR(255) NOT NULL UNIQUE,
    axis VARCHAR(1) NOT NULL
);

-- @block
CREATE TABLE results(
    result_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    axis_x INT NOT NULL,
    axis_y INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- @block
CREATE TABLE hobbys(
    hobby_id INT PRIMARY KEY AUTO_INCREMENT,
    hobby VARCHAR(255) NOT NULL UNIQUE,
    axis_x INT NOT NULL,
    axis_y INT NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE CASCADE
);

-- @block
ALTER TABLE hobbys
ADD COLUMN axis_x INT NOT NULL;

-- @block
ALTER TABLE hobbys
ADD COLUMN axis_y INT NOT NULL;

-- @block
ALTER TABLE hobbys
ADD COLUMN description TEXT;


-- @block
CREATE TABLE categories(
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category VARCHAR(255) NOT NULL UNIQUE
);

-- @block
INSERT into users ( user_id,name,email,password,is_admin )
VALUES (
    "1",
    "admin",
    "admin@admin",
    "admin",
    "1"
);

-- @block
INSERT into questions ( question_id,question,axis )
VALUES (
    "40",
    "Czy wolisz udział w konkursach literackich czy sportowych?",
    "Y"
);

-- @block
select * from results;

-- @block
SELECT * FROM hobbys

-- @block
SELECT * FROM categories

-- @block
SELECT * FROM users

-- @block
SELECT * FROM questions

-- @block
DROP TABLE hobbys

-- @block
INSERT INTO categories (category_id, category) VALUES (1, 'Artystyczne');
INSERT INTO categories (category_id, category) VALUES (2, 'Sportowe');
INSERT INTO categories (category_id, category) VALUES (3, 'Umysłowe');
INSERT INTO categories (category_id, category) VALUES (4, 'Zewnętrzne');
INSERT INTO categories (category_id, category) VALUES (5, 'Technologiczne');

-- @block
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (1, 'Pisanie', -8, -10, 1);
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (2, 'Fotografia', -6, -8, 1);
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (3, 'Malowanie', -9, -9, 1);
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (4, 'Gra w piłkę nożną', 10, 10, 2);
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (5, 'Wspinaczka', 6, 9, 2);
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (6, 'Szachy', -7, -2, 3);
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (7, 'Gry planszowe', -5, -1, 3);
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (8, 'Pływanie', 4, 7, 2);
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (9, 'Wędkowanie', -10, 2, 4);
INSERT INTO hobbys (hobby_id, hobby, axis_x, axis_y, category_id) VALUES (10, 'Programowanie', -5, -6, 5);

-- @block
INSERT INTO questions (question_id, question, axis) VALUES (1, 'Czy wolisz spędzać czas wolny samotnie czy w towarzystwie innych?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (2, 'Czy preferujesz pracę nad projektami samemu czy w zespole?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (3, 'Czy czerpiesz więcej radości z aktywności indywidualnych czy grupowych?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (4, 'Czy wolisz tworzyć sztukę czy uprawiać sport?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (5, 'Czy interesują Cię zajęcia artystyczne czy sportowe?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (6, 'Czy wolisz ćwiczyć samodzielnie czy z partnerem/trenerem?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (7, 'Czy lubisz uczestniczyć w wydarzeniach kulturalnych czy sportowych?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (8, 'Czy preferujesz wystąpienia publiczne czy analizowanie danych w ciszy?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (9, 'Czy wolisz oglądać sztukę czy grać w mecze?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (10, 'Czy łatwiej skupić Ci się w pojedynkę czy w grupie?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (11, 'Czy wolisz eksplorować muzeum czy stadion?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (12, 'Czy cenisz bardziej niezależność czy współpracę?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (13, 'Czy interesuje Cię bardziej projektowanie czy taktyka w sporcie?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (14, 'Czy wolisz organizować własne projekty czy być częścią zespołu?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (15, 'Czy wolisz tworzyć muzykę czy grać w gry zespołowe?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (16, 'Czy wolisz pracować w ciszy czy w hałaśliwym otoczeniu?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (17, 'Czy interesuje Cię bardziej teatr czy siłownia?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (18, 'Czy wolisz wykonywać zadania samodzielnie czy pod nadzorem lidera?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (19, 'Czy wolisz malować czy grać w piłkę?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (20, 'Czy wolisz prowadzić czy być prowadzonym w grupie?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (21, 'Czy wolisz czytać książki czy biegać na świeżym powietrzu?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (22, 'Czy wolisz tworzyć strategie czy współpracować w grupie?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (23, 'Czy interesuje Cię rzeźbiarstwo czy gra w siatkówkę?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (24, 'Czy wolisz spędzać wieczory na pisaniu czy spotkaniach towarzyskich?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (25, 'Czy wolisz projektować czy bawić się w sporty ekstremalne?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (26, 'Czy łatwiej Ci działać w pojedynkę czy z grupą?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (27, 'Czy wolisz tworzyć sztukę cyfrową czy grać w koszykówkę?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (28, 'Czy cenisz bardziej indywidualne osiągnięcia czy sukces zespołu?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (29, 'Czy interesuje Cię bardziej filmowanie czy wspinaczka?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (30, 'Czy wolisz spędzać czas na samotnym spacerze czy w grupie znajomych?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (31, 'Czy wolisz wyrażać siebie poprzez sztukę czy osiągać cele sportowe?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (32, 'Czy łatwiej pracujesz w ciszy czy podczas grupowych burz mózgów?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (33, 'Czy interesują Cię bardziej galerie sztuki czy biegi maratońskie?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (34, 'Czy wolisz wyznaczać cele indywidualne czy zespołowe?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (35, 'Czy wolisz komponować muzykę czy trenować drużynę?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (36, 'Czy cenisz bardziej niezależne decyzje czy demokratyczne procesy grupowe?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (37, 'Czy wolisz szkicować czy grać w gry planszowe?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (38, 'Czy wolisz samotne podróże czy zorganizowane wycieczki grupowe?', 'X');
INSERT INTO questions (question_id, question, axis) VALUES (39, 'Czy wolisz pisać poezję czy trenować boks?', 'Y');
INSERT INTO questions (question_id, question, axis) VALUES (40, 'Czy cenisz bardziej swoje osiągnięcia czy wspólny sukces zespołu?', 'X');


-- @block
CREATE TABLE chatrooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

-- @block
CREATE TABLE messages (
    message_id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    room_id INT,
    user_id INT,
    FOREIGN KEY (room_id) REFERENCES chatrooms(room_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- @block
CREATE TABLE room_participants (
    room_id INT,
    user_id INT,
    PRIMARY KEY (room_id, user_id),
    FOREIGN KEY (room_id) REFERENCES chatrooms(room_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- @block
INSERT INTO chatrooms (room_id, name, created_at, created_by)
VALUES ("5", "Technologiczne", "1970-01-01 10:10:10 ", "1" ),
       ("1", "Artystyczne", "1970-01-01 10:10:10 ", "1" ),
       ("2", "Sportowe", "1970-01-01 10:10:10 ", "1" ),
       ("3", "Umysłowe", "1970-01-01 10:10:10 ", "1" ),
       ("4", "Zewnętrzne", "1970-01-01 10:10:10 ", "1" );

-- @block
UPDATE hobbys
SET description = 'Pisanie to proces wyrażania myśli, uczuć lub informacji za pomocą słów zapisanych na papierze lub w formie cyfrowej.'
WHERE hobby_id = 1;

UPDATE hobbys
SET description = 'Tworzenie obrazów za pomocą aparatu, uchwycenie chwili, emocji lub piękna świata.'
WHERE hobby_id = 2;

UPDATE hobbys
SET description = 'Wyrażanie emocji i wizji poprzez nakładanie farb na płótno lub inną powierzchnię.'
WHERE hobby_id = 3;

UPDATE hobbys
SET description = 'Dynamiczna rywalizacja zespołów polegająca na zdobywaniu goli przy użyciu piłki.'
WHERE hobby_id = 4;

UPDATE hobbys
SET description = 'Pokonywanie pionowych ścian i skał, wymagające siły, techniki i odwagi.'
WHERE hobby_id = 5;

UPDATE hobbys
SET description = 'Strategiczna gra planszowa, w której dwie osoby rywalizują na szachownicy.'
WHERE hobby_id = 6;

UPDATE hobbys
SET description = 'Rozrywka towarzyska polegająca na rywalizacji lub współpracy na planszy z regułami.'
WHERE hobby_id = 7;

UPDATE hobbys
SET description = 'Przemieszczanie się w wodzie za pomocą różnych technik ruchu ciała.'
WHERE hobby_id = 8;

UPDATE hobbys
SET description = 'Cierpliwe łowienie ryb za pomocą wędki, przynęty i odpowiedniej techniki.'
WHERE hobby_id = 9;

UPDATE hobbys
SET description = 'Tworzenie kodu komputerowego, który pozwala maszynom wykonywać określone zadania.'
WHERE hobby_id = 10;

-- @block
ALTER TABLE HOBBYS
ADD long_description TEXT;

-- @block
UPDATE hobbys
SET long_description = 'Pisanie to proces wyrażania myśli, uczuć lub wiedzy za pomocą słów zapisanych na papierze, w dokumencie cyfrowym czy w innej formie trwałej. Jest to fundamentalna umiejętność komunikacyjna, która pozwala na przekazywanie informacji, opowiadanie historii czy dzielenie się refleksjami. Pisanie ma wiele form – od literatury pięknej, takiej jak powieści i wiersze, przez teksty publicystyczne, po raporty naukowe czy dokumenty biznesowe.'
WHERE hobby_id = 1;

UPDATE hobbys  
SET long_description = 'Fotografia to sztuka i technika uchwycenia obrazów za pomocą aparatu, która pozwala zatrzymać chwile, emocje i piękno otaczającego świata. Dzięki wykorzystaniu światła, kompozycji i perspektywy fotografowie tworzą dzieła, które mogą dokumentować rzeczywistość, wywoływać emocje lub służyć jako forma artystycznej ekspresji. Fotografia znajduje zastosowanie w wielu dziedzinach, takich jak reportaż, moda, reklama czy sztuka.'  
WHERE hobby_id = 2;

UPDATE hobbys  
SET long_description = 'Malowanie to forma artystycznego wyrażania siebie, polegająca na nakładaniu farb na różne powierzchnie, takie jak płótno, papier czy mur. Jest to proces twórczy, w którym artysta za pomocą kolorów, faktur i technik, takich jak akwarele, farby olejne czy akryle, tworzy obrazy oddające emocje, idee lub wizje. Malowanie może być zarówno hobby, jak i profesjonalnym zajęciem w dziedzinach takich jak sztuka czy dekoracja.'  
WHERE hobby_id = 3;

UPDATE hobbys  
SET long_description = 'Gra w piłkę nożną to popularny sport zespołowy, który polega na rywalizacji dwóch drużyn dążących do zdobycia większej liczby goli niż przeciwnik. Wymaga świetnej kondycji, współpracy, umiejętności technicznych i strategii. Piłka nożna jest sportem dostępnym na całym świecie, zarówno na poziomie rekreacyjnym, jak i profesjonalnym, a jej popularność łączy ludzi z różnych kultur i środowisk.'  
WHERE hobby_id = 4;

UPDATE hobbys  
SET long_description = 'Wspinaczka to sport i forma rekreacji, która polega na pokonywaniu pionowych ścian skalnych, sztucznych ścianek lub tras górskich. Wymaga siły fizycznej, koncentracji, odwagi i odpowiedniej techniki. Jest doskonałym sposobem na rozwój kondycji, pokonywanie własnych ograniczeń oraz eksplorację natury.'  
WHERE hobby_id = 5;

UPDATE hobbys  
SET long_description = 'Szachy to strategiczna gra planszowa, w której dwóch graczy rywalizuje, przesuwając figury po szachownicy zgodnie z ustalonymi regułami. Celem jest zamatowanie króla przeciwnika. Szachy rozwijają umiejętność logicznego myślenia, planowania i przewidywania ruchów przeciwnika, czyniąc je doskonałym treningiem dla umysłu oraz popularną formą rozrywki intelektualnej.'  
WHERE hobby_id = 6;

UPDATE hobbys  
SET long_description = 'Gry planszowe to różnorodne formy rozrywki towarzyskiej, polegające na rywalizacji lub współpracy graczy na planszy z określonymi zasadami. Mogą mieć charakter edukacyjny, strategiczny, przygodowy czy logiczny, rozwijając takie umiejętności jak myślenie analityczne, praca zespołowa czy kreatywność. Są doskonałym sposobem na spędzanie czasu z rodziną i przyjaciółmi.'  
WHERE hobby_id = 7;

UPDATE hobbys  
SET long_description = 'Pływanie to aktywność fizyczna i forma rekreacji, która polega na przemieszczaniu się w wodzie za pomocą różnych technik, takich jak kraul, żabka czy styl grzbietowy. Jest to sport wszechstronnie rozwijający organizm, poprawiający kondycję, wzmacniający mięśnie i korzystnie wpływający na zdrowie psychiczne. Pływanie może być uprawiane zarówno rekreacyjnie, jak i zawodowo.'  
WHERE hobby_id = 8;

UPDATE hobbys  
SET long_description = 'Wędkowanie to hobby i forma rekreacji, która polega na łowieniu ryb przy użyciu wędki, żyłki, przynęty i odpowiedniej techniki. Jest to zajęcie, które łączy cierpliwość, precyzję i znajomość natury, oferując jednocześnie relaks i kontakt z przyrodą. Dla wielu osób wędkowanie to również sposób na medytację i oderwanie się od codziennych trosk.'  
WHERE hobby_id = 9;

UPDATE hobbys  
SET long_description = 'Programowanie to proces tworzenia kodu komputerowego, który instruuje maszyny, jak realizować określone zadania. Wymaga znajomości języków programowania, takich jak Python, Java czy C++, a także umiejętności analitycznego myślenia i rozwiązywania problemów. Programowanie znajduje zastosowanie w tworzeniu aplikacji, stron internetowych, gier czy systemów operacyjnych, stanowiąc kluczowy element współczesnej technologii.'  
WHERE hobby_id = 10;
