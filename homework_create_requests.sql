create table if not exists genre(
genre_id serial primary key,
genre_name varchar(60) unique not null
);


create table if not exists singer(
singer_id serial primary key,
singer_name varchar(60) not null
);


create table if not exists singer_genre(
singer_id integer references singer(singer_id),
genre_id integer references genre(genre_id),
constraint pk1 primary key(genre_id, singer_id)
);



create table if not exists album(
album_id serial primary key,
album_name varchar(60) not null,
album_year integer not null,
check(album_year > 1900)
);


create table if not exists singer_album(
album_id integer references album(album_id),
singer_id integer references singer(singer_id),
constraint pk primary key(singer_id, album_id)
);


create table if not exists collection(
collection_id serial primary key,
collection_name varchar(60) not null,
collection_year integer not null,
check(collection_year > 1900)
);


create table if not exists collection_track(
collection_id integer references collection(collection_id),
track_id integer references track(track_id)
);

create table if not exists track(
track_id serial primary key,
track_name varchar(60) not null,
duration integer not null,
album_id integer references album(album_id)
);






