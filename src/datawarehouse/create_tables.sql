CREATE TABLE public.staging_prices (
	vegetable_id integer NOT NULL,
    vegetable_name varchar(255) NOT NULL,
    price numeric(18) NOT NULL,
    month integer NOT NULL, 
    year integer NOT NULL,
    day integer NOT NULL,
);

CREATE TABLE public.staging_sensors (
    average numeric(18),
    maximum numeric(18), 
    minimum numeric(18), 
    median numeric(18), 
    station_code integer, 
    sensor_code integer,
    date timestamp, 
    station_name varchar, 
    state varchar, 
    town varchar, 
    zone varchar,
    latitude numeric(18,0),
	longitude numeric(18,0),
);

/*
CREATE TABLE public.location (
	location_id int NOT NULL,
	latitude numeric(18,0),
	longitude numeric(18,0),
    state varchar(256),
    town varchar(256),
);

CREATE TABLE public.songplays (
	playid varchar(32) NOT NULL,
	start_time timestamp NOT NULL,
	userid int4 NOT NULL,
	"level" varchar(256),
	songid varchar(256),
	artistid varchar(256),
	sessionid int4,
	location varchar(300),
	user_agent varchar(256),
	CONSTRAINT songplays_pkey PRIMARY KEY (playid)
);

CREATE TABLE public.songs (
	songid varchar(256) NOT NULL,
	title varchar(300),
	artistid varchar(256),
	"year" int4,
	duration numeric(18,0),
	CONSTRAINT songs_pkey PRIMARY KEY (songid)
);

CREATE TABLE public.staging_events (
	artist varchar(256),
	auth varchar(256),
	firstname varchar(256),
	gender varchar(256),
	iteminsession int4,
	lastname varchar(256),
	length numeric(18,0),
	"level" varchar(256),
	location varchar(256),
	"method" varchar(256),
	page varchar(256),
	registration numeric(18,0),
	sessionid int4,
	song varchar(256),
	status int4,
	ts int8,
	useragent varchar(256),
	userid int4
);

CREATE TABLE public.staging_songs (
	num_songs int4,
	artist_id varchar(256),
	artist_name varchar(400),
	artist_latitude numeric(18,0),
	artist_longitude numeric(18,0),
	artist_location varchar(300),
	song_id varchar(256),
	title varchar(300),
	duration numeric(18,0),
	"year" int4
);

CREATE TABLE public."time" (
	start_time timestamp NOT NULL,
	"hour" int4,
	"day" int4,
	week int4,
	"month" varchar(256),
	"year" int4,
	weekday varchar(256),
	CONSTRAINT time_pkey PRIMARY KEY (start_time)
) ;

CREATE TABLE public.users (
	userid int4 NOT NULL,
	first_name varchar(256),
	last_name varchar(256),
	gender varchar(256),
	"level" varchar(256),
	CONSTRAINT users_pkey PRIMARY KEY (userid)
);
*/