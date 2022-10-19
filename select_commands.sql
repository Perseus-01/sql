--название и год выхода альбомов, вышедших в 2018 году;

select album_name, album_year 
from album a 
where album_year = 2018;

-- название и продолжительность самого длительного трека;

select track_name, duration 
from track t 
order by duration desc limit 1;

--название треков, продолжительность которых не менее 3,5 минуты

select track_name
from track t 
where duration >= 210;

-- названия сборников, вышедших в период с 2018 по 2020 год включительно

select collection_name 
from collection c 
where collection_year between 2018 and 2020;

--исполнители, чье имя состоит из 1 слова
select singer_name 
from singer s 
where not singer_name  like '%% %%'  --этого не было в презетации, лекции. FYI

--название треков, которые содержат слово "мой"/"my"

select track_name 
from track t 
where track_name like '%my%'

