INSERT INTO perfomers VALUES
('1','MakSim'),
('2','PHARAOH'),
('3','Nature'),
('4','39');

INSERT INTO music_genres VALUES
('1','cloud'),
('2','pop'),
('3','Classic'),
('4','Natural');

INSERT INTO albums(name, date_of_creation) VALUES
('Tvoya','2007-01-01'),
('PSIH','2014-01-06'),
('Nature','0010-10-10'),
('Together','2023-12-05');

INSERT INTO list_of_tracks(track_id, album, track_name, duration) VALUES
('1','1','Znaesh_li_ti','00:03:20'),
('2','1','Doroga','00:05:00'),
('3','1','Nezhny_vozrast','00:02:50'),
('4','2','Son','00:03:20'),
('5','2','V_zone','00:02:20'),
('6','3','Zvuk_dozhd','03:03:20'),
('7','3','Zvuk_petuha','00:01:20'),
('999','4','Poem_vmeste','00:23:20'),
('500','4','Kon','01:01:01');

INSERT INTO collections(name, date_of_creation) VALUES
('Moe','2007-02-01'),
('Tvoe','2008-02-01'),
('Ego','2009-02-01'),
('Nashe','2027-02-01');

INSERT INTO tracks_col(tracksid, collectionid) VALUES
('1','1'),
('2','1'),
('3','1'),
('1','2'),
('4','2'),
('5','2'),
('1','3'),
('2','3'),
('5','3'),
('6','3'),
('999','3'),
('500','3'),
('7','3'),
('1','4'),
('6','4'),
('5','4'),
('2','4'),
('3','4');

INSERT INTO genre_perf VALUES
('2','1'),
('4','1'),
('2','2'),
('1','2'),
('4','2'),
('1','3'),
('2','3'),
('3','3'),
('4','3'),
('3','4');

INSERT INTO perfomers_albums(perfomer, album) VALUES
('1','1'),
('2','2'),
('4','2'),
('3','3'),
('1','4'),
('2','4'),
('3','4'),
('4','4');


INSERT INTO list_of_tracks VALUES
('8','1','my','00:05:00'),
('9','2','Мое эго','00:05:00');

INSERT INTO collections(name, date_of_creation) VALUES
('Их','2020-02-01'),
('Всех','2019-02-01');

INSERT INTO tracks_col(tracksid, collectionid) VALUES
('8','5'),
('8','6'),
('9','5'),
('9','1'),
('3','6'),
('4','6');

INSERT INTO albums(name, date_of_creation) VALUES
('Ничья','2020-01-01'),
('Победа','2019-01-06');

INSERT INTO list_of_tracks VALUES
('10','6','EEEEmy','00:01:00'),
('11','6','Мое дело','03:05:00'),
('12','5','куеиееууке','00:00:50');

INSERT INTO perfomers_albums(perfomer, album) VALUES
('1','5'),
('1','6'),
('2','5');

INSERT INTO tracks_col(tracksid, collectionid) VALUES
('10','1'),
('10','2'),
('10','5'),
('11','2'),
('11','6'),
('11','5');