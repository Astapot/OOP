CREATE TABLE IF NOT EXISTS Music_genres(
	Genre_id SERIAL PRIMARY KEY,
	Name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Perfomers(
	Perfomer_id SERIAL PRIMARY KEY,
	Nickname VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genre_Perf(
	genre_id INTEGER REFERENCES Music_genres(Genre_id),
	perfomer_id INTEGER REFERENCES Perfomers(Perfomer_id),
	CONSTRAINT Gen_Per PRIMARY KEY (genre_id, perfomer_id)
);

CREATE TABLE IF NOT EXISTS Albums(
	Album_id SERIAL PRIMARY KEY,
	Name VARCHAR NOT NULL,
	Date_of_creation DATE
);

CREATE TABLE IF NOT EXISTS Perfomers_Albums(
	UniqueID SERIAL PRIMARY KEY,
	Perfomer INTEGER REFERENCES Perfomers(Perfomer_id),
	Album INTEGER REFERENCES Albums(Album_id)
);

CREATE TABLE IF NOT EXISTS List_of_tracks(
	Track_id SERIAL PRIMARY KEY,
	Album INTEGER REFERENCES Albums(Album_id),
	Track_name VARCHAR(100) NOT NULL,
	Duration TIME NOT NULL
);

CREATE TABLE IF NOT EXISTS Collections(
	Collection_id SERIAL PRIMARY KEY,
	Name VARCHAR(100) NOT NULL,
	Date_of_creation DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Tracks_Col(
	UniqueID SERIAL PRIMARY KEY,
	TracksID INTEGER REFERENCES List_of_tracks(Track_id),
	CollectionID INTEGER REFERENCES Collections(Collection_id)
);	

ALTER TABLE Collections ALTER COLUMN Date_of_creation TYPE TIMESTAMP;