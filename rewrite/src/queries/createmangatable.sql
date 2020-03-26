CREATE TABLE IF NOT EXISTS manga (
id serial PRIMARY KEY NOT NULL,
title VARCHAR(255),
url VARCHAR(255),
latest_chapter REAL,
chapters_read REAL,
status SMALLINT
);