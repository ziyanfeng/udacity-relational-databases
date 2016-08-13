-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE DATABASE tournament;
\c tournament;

-- TABLE players records players information
CREATE TABLE players
(
player_id SERIAL PRIMARY KEY,
name VARCHAR(30) NOT NULL,
wins INTEGER DEFAULT 0,
matches INTEGER DEFAULT 0
);


-- TABLE matches records match record
CREATE TABLE matches
(
match_id SERIAL PRIMARY KEY,
winner_id INTEGER,
loser_id INTEGER,
FOREIGN KEY (winner_id) REFERENCES players(player_id),
FOREIGN KEY (loser_id) REFERENCES players(player_id)
);



