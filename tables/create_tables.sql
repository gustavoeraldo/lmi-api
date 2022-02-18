create table users(
	id SERIAL PRIMARY KEY,
	first_name VARCHAR(40) NOT NULL,
	last_name VARCAHR(40) NOT NULL,
	email VARCAHR(60) NOT NULL,
	hashed_password VARCHAR NOT NULL,
	user_type INT NOT NULL,
	is_active BOOLEAN DEFAULT 'true',
	created_at TIMESTAMPTZ DEFAULT NOW(),
	updated_at TIMESTAMPTZ DEFAULT NULL,
	deleted_at TIMESTAMPTZ DEFAULT NULL
);


CREATE TABLE value_types(
	id SERIAL PRIMARY KEY,
	description TEXT(100) UNIQUE
);

CREATE TABLE measurements(
	id BIGSERIAL PRIMARY KEY,
	type_id INT NOT NULL REFERENCES value_types(id),
	user_id INT NOT NULL REFERENCES users(id),
	measure FLOAT,
	tag VARCHAR(30),
	created_at TIMESTAMPTZ DEFAULT NOW(),
	deleted_at TIMESTAMPTZ DEFAULT NULL
);