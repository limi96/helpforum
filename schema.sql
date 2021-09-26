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
	user_id INTEGER REFERENCES users ON DELETE CASCADE,
	send_time TIMESTAMP
);

CREATE TABLE answers (
	id SERIAL PRIMARY KEY,
	answer_content TEXT,
	answer_points INTEGER,
	question_id INTEGER REFERENCES user_questions ON DELETE CASCADE,
	user_id INTEGER REFERENCES users ON DELETE CASCADE,
	send_time TIMESTAMP	
);

CREATE TABLE points (
  result INTEGER,
  answer_id INTEGER REFERENCES answers ON DELETE CASCADE,
  user_id INTEGER REFERENCES users ON DELETE CASCADE
);


