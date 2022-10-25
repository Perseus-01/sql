--1. количество исполнителей в каждом жанре;

select genre_id, count(singer_id) as singer_number
from singer_genre sg 
group by genre_id
order by genre_id 


--2. количество треков, вошедших в альбомы 2019-2020 годов;

select count(track_id) as tracks_2019_2020
from track t 
join album a on t.album_id = a.album_id 
where album_year between 2019 and 2020

--3. cредняя продолжительность треков по каждому альбому;
select album_id, round(avg(duration), 0) as avg_track_duration
from track t
group by album_id
order by album_id 

--4. все исполнители, которые не выпустили альбомы в 2020 году;
select singer_name as singer_no_album_in_2020
from singer s
join singer_album sa on s.singer_id = sa.singer_id 
join album a on sa.album_id = a.album_id 
where album_year != 2020
order by singer_name 

--5. названия сборников, в которых присутствует конкретный исполнитель (выберите сами - Zivert)

select collection_name as Zivert_collections
from collection c 
join collection_track ct on c.collection_id = ct.collection_id 
join track t on ct.track_id = t.track_id 
join album a on t.album_id = a.album_id 
join singer_album sa on a.album_id = sa.album_id 
join singer s on sa.singer_id = s.singer_id 
where singer_name = 'Zivert'

--6. название альбомов, в которых присутствуют исполнители более 1 жанра;
select album_name
from album a 
join singer_album sa on a.album_id = sa.album_id 
join singer s on sa.singer_id = s.singer_id 
join singer_genre sg on sa.singer_id = s.singer_id
join genre g on sg.genre_id = g.genre_id 
group by album_name 
having count(g.genre_name) > 1
order by album_name

--7. наименование треков, которые не входят в сборники;

select track_name as tracks_not_in_collections
from track t 
left join collection_track ct on ct.track_id = t.track_id 
where ct.track_id is null

--8. исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько)
select s.singer_name, t.duration 
from singer s 
join singer_album sa on s.singer_id = sa.singer_id 
join album a on sa.album_id = a.album_id 
join track t on a.album_id = t.track_id 
group by s.singer_name, t.duration
having t.duration = (
	select min(duration) from track t)

--9. название альбомов, содержащих наименьшее количество треков
select distinct  album_name 
from album a 
join track t on a.album_id = t.track_id 
where t.album_id in (
    select album_id
    from track
    group by album_id
    having count(track_id) = (
        select count(track_id)
        from track
        group by album_id
        order by count
        limit 1
    )
)



