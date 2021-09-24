CREATE TABLE users (	
	id SERIAL PRIMARY KEY, 
	username VARCHAR(144),
	password VARCHAR(144),
	creation_time TIMESTAMP
);

CREATE TABLE user_questions (
	id SERIAL PRIMARY KEY,
	question_title TEXT,
	question_content TEXT,
	user_id INTEGER REFERENCES users,
	send_time TIMESTAMP
);

CREATE TABLE answers (
	id SERIAL PRIMARY KEY,
	answer_content TEXT,
	question_id INTEGER REFERENCES user_questions,
	user_id INTEGER REFERENCES users,
	send_time TIMESTAMP
);