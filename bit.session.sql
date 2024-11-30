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
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- @block
CREATE TABLE hobbys(
    hobby_id INT PRIMARY KEY AUTO_INCREMENT,
    hobby VARCHAR(255) NOT NULL UNIQUE,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

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
SELECT * FROM questions
