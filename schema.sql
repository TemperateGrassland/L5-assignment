-- //Todo remove these drop table statements - the application requires test data

DROP TABLE IF EXISTS fact;
DROP TABLE IF EXISTS factDetail;
DROP TABLE IF EXISTS source;
DROP TABLE IF EXISTS user;

CREATE TABLE fact (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    left_entity varchar(255) NOT NULL,
    relation_entity varchar(255) NOT NULL,
    right_entity varchar(255) NOT NULL,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES factDetail (fact_id),
    FOREIGN KEY (author_id) REFERENCES user (userid)
);

CREATE TABLE factDetail (
    fact_id int NOT NULL,
    unique_fact BOOL NOT NULL,
    metafact BOOL NOT NULL,
    believed_status BOOL NOT NULL,
    url varchar(255) NOT NULL,
    FOREIGN KEY (url) REFERENCES source (url)
);

CREATE TABLE source (
    url varchar(255) NOT NULL,
    username varchar(255) NOT NULL,
    FOREIGN KEY (username) REFERENCES user (username)
);

CREATE TABLE user (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    firstname varchar(255) NOT NULL,
    lastname varchar(255) NOT NULL,
    admin BOOL NOT NULL
);

INSERT INTO user (username, password, firstname, lastname, admin) VALUES ('guestuser', 'password', 'admin', 'user', false);
INSERT INTO user (username, password, firstname, lastname, admin) VALUES ('adminuser', 'password', 'admin', 'user', true);
INSERT INTO user (username, password, firstname, lastname, admin) VALUES ('testuser', 'password', 'test', 'user', false);
INSERT INTO fact (left_entity, relation_entity, right_entity, author_id) VALUES ("paris", "is the capital of", "france", 2);
INSERT INTO fact (left_entity, relation_entity, right_entity, author_id) VALUES ("the sky", "is the colour", "blue", 2);
INSERT INTO fact (left_entity, relation_entity, right_entity, author_id) VALUES ("orange juice", "has the molecular state of", "liquid", 2);
INSERT INTO fact (left_entity, relation_entity, right_entity, author_id) VALUES ("the Italy mens national football team ", "came first place at", "UEFA Euro 2020", 2);
INSERT INTO fact (left_entity, relation_entity, right_entity, author_id) VALUES ("kimchi", "is an instance of", "food", 2);
INSERT INTO fact (left_entity, relation_entity, right_entity, author_id) VALUES ("eagle", "is an instance of", "bird", 2);