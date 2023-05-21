-- ЗАДАНИЕ 2.1

SELECT track_name, duration
FROM list_of_tracks
WHERE duration = (SELECT MAX(duration) FROM list_of_tracks)
ORDER BY track_name;
-- два одинаковых запроса, просто попробовал
SELECT track_name, duration
FROM list_of_tracks
ORDER BY duration DESC
LIMIT 1;

-- ЗАДАНИЕ 2.2


SELECT track_name, duration
FROM list_of_tracks
WHERE duration >= '00:03:30';

-- ЗАДАНИЕ 2.3

SELECT name
FROM collections
WHERE date_of_creation BETWEEN '2018-01-01' AND '2020-12-31';

-- ЗАДАНИЕ 2.4

SELECT nickname
FROM perfomers
WHERE nickname NOT LIKE '% %';

-- ЗАДАНИЕ 2.5

SELECT track_name
FROM list_of_tracks
WHERE track_name ILIKE 'my %' 
OR track_name ILIKE '% my'
OR track_name ILIKE '% my %'
OR track_name ILIKE 'my'
OR track_name ILIKE 'Мой %'
OR track_name ILIKE '% Мой'
OR track_name ILIKE '% Мой %'
OR track_name ILIKE 'Мой';

--ЗАДАНИЕ 2.5 вариант 2

SELECT track_name
FROM list_of_tracks
WHERE string_to_array(lower(track_name), ' ') && ARRAY['my', 'мой'];

-- ЗАДАНИЕ 3.1

SELECT name, COUNT(perfomer_id) FROM music_genres mg
LEFT JOIN genre_perf gp ON mg.genre_id  = gp.genre_id 
GROUP BY mg.genre_id , mg.name
ORDER BY mg.genre_id;

-- ЗАДАНИЕ 3.2

SELECT COUNT(track_id) FROM albums a 
JOIN list_of_tracks lot ON lot.album = a.album_id 
WHERE date_of_creation BETWEEN '2019-01-01' AND '2020-12-31';


-- ЗАДАНИЕ 3.3

SELECT name, AVG(duration) FROM albums a
JOIN list_of_tracks lot ON lot.album = a.album_id
GROUP BY a.album_id, a.name
ORDER BY a.album_id;

-- Задание 3.4

SELECT nickname FROM perfomers
WHERE nickname NOT IN 
(
SELECT nickname FROM perfomers p
JOIN perfomers_albums pa ON pa.perfomer = p.perfomer_id
JOIN albums a ON pa.album = a.album_id
WHERE a.date_of_creation BETWEEN '2020-01-01' AND '2020-12-31'
GROUP BY p.perfomer_id, p.nickname
ORDER BY p.perfomer_id
);

--Задание 3.5 Исполнитель - Nature


SELECT DISTINCT c.name FROM perfomers p
JOIN perfomers_albums pa ON pa.perfomer = p.perfomer_id 
JOIN albums a ON pa.album = a.album_id 
JOIN list_of_tracks lot ON lot.album = a.album_id
JOIN tracks_col tc ON tc.tracksid = lot.track_id
JOIN collections c ON c.collection_id = tc.collectionid
WHERE p.nickname = 'Nature'
GROUP by c.name;

