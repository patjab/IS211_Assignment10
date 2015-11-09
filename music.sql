/*
	AUTHOR: PATRICK ABEJAR

	This SQL query represents data with regards to Artists,
    their albums, and the songs that are contained in their
    album. The relationship made between Artists-Albums is
	one-to-many (one artist can have multiple albums, but
    an album may only have one artist per the assignment.)
    The relationship made between Albums-Song is one-to-
    many as well as many songs may be contained within an
    album but there is only one album associated with each
    song.
    
    DUE to the fact that there are no many-to-many relation-
    ships that exist, the relational key may be placed in
    the tables directly where the ID of the associated art-
    ist in a particular album is a separate column while
    and IDs of associated albums are entered as a separate
    column in the songs table.
    
    A relational table isn't necesary as all the relation-
    ships are one-to-many.
*/

DROP TABLE IF EXISTS Artists;
DROP TABLE IF EXISTS Albums;
DROP TABLE IF EXISTS Songs;

CREATE TABLE Artists (
	id INTEGER PRIMARY KEY,
	name TEXT
);

CREATE TABLE Albums (
	id INTEGER PRIMARY KEY,
    name TEXT,
    artistID INTEGER
);

CREATE TABLE Songs (
	id INTEGER PRIMARY KEY,
    name TEXT,
    albumID INTEGER,
    trackNumber INTEGER,
    duration INTEGER
);