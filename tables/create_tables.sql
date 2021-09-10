create table users(
	usr_id SERIAL PRIMARY KEY,
	username varchar(60)
);

CREATE TABLE value_types(
	m_type_id SERIAL PRIMARY KEY,
	description text(255) UNIQUE
);

CREATE TABLE measurements(
	measure_id BIGSERIAL PRIMARY KEY,
	type_id INT NOT NULL REFERENCES value_types(m_type_id),
	user_id INT NOT NULL REFERENCES users(usr_id),
	measure FLOAT,
	tag VARCHAR(30),
	created_at TIMESTAMPTZ DEFAULT NOW(),
	deleted_at TIMESTAMPTZ
);