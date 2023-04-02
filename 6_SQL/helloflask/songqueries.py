from sqlalchemy import select
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import registry,subqueryload, joinedload
from sqlalchemy.sql import func, text


from song_db import Base, engine, db_session
from songmodels import Album, Song, Artist, SongArtist, SongRank, User

################################################################3
# Album, Song table creation and data addtion to table (Done)
# Album.__table__.create(bind=engine, checkfirst=True)
# Song.__table__.create(bind=engine, checkfirst=True)
# Artist.__table__.create(bind=engine, checkfirst=True)
# SongArtist.__table__.create(bind=engine, checkfirst=True)
# SongRank.__table__.create(bind=engine, checkfirst=True)
# User.__table__.create(bind=engine, checkfirst=True)

################################################################3
# data addtion to Album table (Done)
# album_list=Album(albumid='0000001', createdt='2018-8-28',
#                  title='Ditto', company='신나라', genre='발라드',
#                  likecnt=1200, rate=3.5, crawldt='2018-8-28')
# db_session.add(album_list)

# album_list=Album(albumid='0000002', createdt='2018-8-28',
#                  title='OMG', company='신나라', genre='Jazz',
#                  likecnt=1500, rate=4.0, crawldt='2022-8-28')
# db_session.add(album_list)

# album_list=Album(albumid='0000003', createdt='2018-9-28',
#                  title='OMG2', company='신나라2', genre='Dance',
#                  likecnt=1100, rate=4.5, crawldt='2022-9-28')
# db_session.add(album_list)
# db_session.commit()

# album_list=Album(albumid='0000004', createdt='2017-01-07',
#                  title='도깨비 OST Part 3', company='Stone Music Entertainment', genre='Drama',
#                  likecnt=23213, rate=4.6, crawldt='2017-10-07')
# db_session.add(album_list)

# album_list=Album(albumid='0000005', createdt='2017-02-13',
#                  title='YOU NEVER WALK ALONE', company='빅히트 엔터테인먼트', genre='Hip-Hop',
#                  likecnt=129576, rate=4.6, crawldt='2017-11-07')
# db_session.add(album_list)

# album_list=Album(albumid='0000006', createdt='2017-03-24',
#                  title='밤편지', company='카카오 미디어', genre='Balad',
#                  likecnt=392576, rate=4.9, crawldt='2017-04-07')
# db_session.add(album_list)

# album_list=Album(albumid='0000007', createdt='2017-07-10',
#                  title='Moonlight', company='인포페이퍼', genre='Balad',
#                  likecnt=162576, rate=4.0, crawldt='2017-08-10')
# db_session.add(album_list)

# album_list=Album(albumid='0000008', createdt='2017-08-07',
#                  title='TO BE ONE', company='YMC엔터테인먼트', genre='Dance, Balad',
#                  likecnt=128376, rate=4.0, crawldt='2017-08-20')
# db_session.add(album_list)

# album_list=Album(albumid='0000009', createdt='2017-08-18',
#                  title='LOVE YOURSELF', company='빅히트 엔터테인먼트', genre='Rap, Hip-Hop',
#                  likecnt=143576, rate=4.3, crawldt='2017-08-20')
# db_session.add(album_list)

# album_list=Album(albumid='0000010', createdt='2017-10-14',
#                  title='겨울 안부', company='먼데이키즈 컴퍼니', genre='Balad',
#                  likecnt=6134, rate=4.3, crawldt='2017-10-24')
# db_session.add(album_list)

# album_list=Album(albumid='0000011', createdt='2017-10-16',
#                  title='Brother Act', company='큐브앤 엔터테인먼트', genre='Balad, Dance, R&B, Soul',
#                  likecnt=49448, rate=4.6, crawldt='2017-10-24')
# db_session.add(album_list)

# album_list=Album(albumid='0000012', createdt='2017-10-31',
#                  title='About You', company='닐로 컴퍼니', genre='Balad',
#                  likecnt=7894, rate=3.2, crawldt='2017-10-24')
# db_session.add(album_list)

# album_list=Album(albumid='0000013', createdt='2018-11-05',
#                  title='Everyday is Christmams', company='Monday Puzzle Atlantic', genre='Pop',
#                  likecnt=8533, rate=3.7, crawldt='2018-11-24')
# db_session.add(album_list)

# album_list=Album(albumid='0000014', createdt='2017-11-13',
#                  title='NOTHING WITHOUT YOU', company='YMC 엔터테인먼트', genre='Dance, Balad',
#                  likecnt=91439, rate=3.6, crawldt='2018-11-24')
# db_session.add(album_list)

# album_list=Album(albumid='0000015', createdt='2017-11-28',
#                  title='그날처럼', company='리메즈', genre='Balad',
#                  likecnt=91439, rate=4.9, crawldt='2018-12-24')
# db_session.add(album_list)
# db_session.commit()

################################################################3
# data addtion to song table (Done)
# song_list=Song(songno='0000001', title='피어나도록 (love you twice)',
#                  genre='발라드', likecnt=3206, albumid='0000001')
# db_session.add(song_list)

# song_list=Song(songno='0000002', title='피어나도록2 (love you twice)',
#                  genre='발라드', likecnt=3208, albumid='0000001')
# db_session.add(song_list)

# song_list=Song(songno='0000003', title='피어나도록3 (love you twice)',
#                  genre='발라드', likecnt=3200, albumid='0000001')
# db_session.add(song_list)

# song_list=Song(songno='0000004', title='Hype boy',
#                  genre='Jazz', likecnt=3200, albumid='0000002')
# db_session.add(song_list)

# song_list=Song(songno='0000005', title='Teddy Bear',
#                  genre='Jazz', likecnt=3200, albumid='0000002')
# db_session.add(song_list)


# song_list=Song(songno='0000006', title='Happy new year',
#                  genre='Dance', likecnt=3200, albumid='0000003')
# db_session.add(song_list)

# song_list=Song(songno='0000007', title='Happy new year2',
#                  genre='Dance', likecnt=3200, albumid='0000003')
# db_session.add(song_list)

# db_session.commit()

# song_list=Song(songno='0000008', title='봄날',
#                  genre='Rap/Hip-Hop', likecnt=305832, albumid='0000009')
# db_session.add(song_list)

# song_list=Song(songno='0000009', title='밤편지',
#                  genre='Balad', likecnt=405832, albumid='0000006')
# db_session.add(song_list)

# song_list=Song(songno='0000010', title='선물',
#                  genre='Balad', likecnt=273948, albumid='0000010')
# db_session.add(song_list)

# song_list=Song(songno='0000011', title='에너제틱',
#                  genre='Balad', likecnt=287338, albumid='0000014')
# db_session.add(song_list)

# song_list=Song(songno='0000012', title='DNA',
#                  genre='Balad', likecnt=287338, albumid='0000012')
# db_session.add(song_list)

# song_list=Song(songno='0000013', title='겨울안부',
#                  genre='Balad', likecnt=127226, albumid='0000007')
# db_session.add(song_list)

# song_list=Song(songno='0000014', title='그리워하다',
#                  genre='Balad', likecnt=127226, albumid='0000010')
# db_session.add(song_list)

# song_list=Song(songno='0000015', title='지나오다',
#                  genre='Balad', likecnt=193432, albumid='0000015')
# db_session.add(song_list)

# song_list=Song(songno='0000016', title='Snowman',
#                  genre='Pop', likecnt=193432, albumid='0000013')
# db_session.add(song_list)

# song_list=Song(songno='0000017', title='Beautiful',
#                  genre='Dance', likecnt=193432, albumid='0000014')
# db_session.add(song_list)

# song_list=Song(songno='0000018', title='그날처럼',
#                  genre='Deama', likecnt=293432, albumid='0000004')
# db_session.add(song_list)

# song_list=Song(songno='0000019', title='Universe',
#                  genre='Hip-Hop', likecnt=193432, albumid='0000005')
# db_session.add(song_list)

# song_list=Song(songno='0000020', title='Universe2',
#                  genre='Dance', likecnt=193432, albumid='0000008')
# db_session.add(song_list)

# song_list=Song(songno='0000021', title='Universe3',
#                  genre='R&B', likecnt=193432, albumid='0000011')
# db_session.add(song_list)
# db_session.commit()

################################################################3
# data addtion to Artist table (Done)
# artist_list=Artist(artistid='0000001', name='권소현',
#                  atype=1)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000002', name='황진하',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000003', name='황규성',
#                  atype=1)
# db_session.add(artist_list)
# db_session.commit()

# artist_list=Artist(artistid='0000004', name='김보아',
#                  atype=1)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000005', name='금수현',
#                  atype=1)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000006', name='김장우',
#                  atype=1)
# db_session.add(artist_list)


# artist_list=Artist(artistid='0000007', name='김재훈',
#                  atype=1)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000008', name='류재준',
#                  atype=1)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000009', name='백병동',
#                  atype=1)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000010', name='안익태',
#                  atype=1)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000011', name='윤이상',
#                  atype=1)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000012', name='이신우',
#                  atype=1)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000013', name='빅뱅',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000014', name='용감한 형제',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000015', name='김도현',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000016', name='Perry',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000017', name='Teddy',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000018', name='최필강',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000019', name='KUSH',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000020', name='노브레인',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000021', name='이영훈',
#                  atype=2)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000022', name='빅뱅3',
#                  atype=3)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000023', name='용감한 형제3',
#                  atype=3)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000024', name='김도현3',
#                  atype=3)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000025', name='Perry3',
#                  atype=3)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000026', name='Teddy3',
#                  atype=3)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000027', name='최필강3',
#                  atype=3)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000028', name='KUSH3',
#                  atype=3)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000029', name='노브레인3',
#                  atype=3)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000030', name='이영훈3',
#                  atype=3)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000031', name='빅뱅4',
#                  atype=4)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000032', name='용감한 형제4',
#                  atype=4)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000033', name='김도현4',
#                  atype=4)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000034', name='Perry4',
#                  atype=4)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000035', name='Teddy4',
#                  atype=4)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000036', name='최필강4',
#                  atype=4)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000037', name='KUSH4',
#                  atype=4)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000038', name='노브레인4',
#                  atype=4)
# db_session.add(artist_list)

# artist_list=Artist(artistid='0000039', name='이영훈4',
#                  atype=4)
# db_session.add(artist_list)

# db_session.commit()



################################################################3
# data addtion to SongArtist table (Done)
# songartist_list=SongArtist(songno='0000001', artistid='0000001',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000002', artistid='0000002',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000003', artistid='0000002',
#                  atype=1)
# db_session.add(songartist_list)
# db_session.commit()

# songartist_list=SongArtist(songno='0000001', artistid='0000001',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000001', artistid='0000013',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000001', artistid='0000022',
#                  atype=3)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000001', artistid='0000031',
#                  atype=4)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000002', artistid='0000002',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000002', artistid='0000014',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000002', artistid='0000023',
#                  atype=3)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000002', artistid='0000032',
#                  atype=4)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000003', artistid='0000003',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000003', artistid='0000015',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000003', artistid='0000024',
#                  atype=3)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000003', artistid='0000033',
#                  atype=4)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000004', artistid='0000004',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000004', artistid='0000016',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000004', artistid='0000025',
#                  atype=3)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000004', artistid='0000034',
#                  atype=4)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000005', artistid='0000005',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000005', artistid='0000017',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000005', artistid='0000026',
#                  atype=3)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000005', artistid='0000035',
#                  atype=4)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000006', artistid='0000006',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000006', artistid='0000018',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000006', artistid='0000027',
#                  atype=3)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000006', artistid='0000036',
#                  atype=4)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000007', artistid='0000007',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000007', artistid='0000019',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000007', artistid='0000028',
#                  atype=3)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000007', artistid='0000037',
#                  atype=4)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000008', artistid='0000008',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000008', artistid='0000020',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000008', artistid='0000029',
#                  atype=3)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000008', artistid='0000038',
#                  atype=4)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000009', artistid='0000009',
#                  atype=1)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000009', artistid='0000021',
#                  atype=2)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000009', artistid='0000030',
#                  atype=3)
# db_session.add(songartist_list)

# songartist_list=SongArtist(songno='0000009', artistid='0000039',
#                  atype=4)
# db_session.add(songartist_list)

# db_session.commit()


################################################################3
# data addtion to SongRank table (Done)
# songrank_list = SongRank(id=1, rankdt='2022-9-28',songno='0000001',srank=1)
# db_session.add(songrank_list)

# songrank_list = SongRank(id=2, rankdt='2022-9-20',songno='0000002',srank=2)
# db_session.add(songrank_list)

# songrank_list = SongRank(id=3, rankdt='2022-10-28',songno='0000003',srank=3)
# db_session.add(songrank_list)

songrank_list = SongRank(id=4, rankdt='2022-10-28',songno='0000004',srank=4)
db_session.add(songrank_list)

songrank_list = SongRank(id=5, rankdt='2022-10-28',songno='0000005',srank=5)
db_session.add(songrank_list)

songrank_list = SongRank(id=6, rankdt='2022-10-28',songno='0000006',srank=6)
db_session.add(songrank_list)

db_session.commit()


#################################################################3
# # data addtion to SongRank table (Done)
# from sqlalchemy.orm import subqueryload, joinedload
# ret = Song.query.options(joinedload(Song.album)).filter(Song.likecnt < 10000).options(joinedload(Song.songartists)).options(
#         subqueryload(Song.songartists, SongArtist.artist)).order_by(text('atype'))

# print(ret)

#################################################################3
# User data creation
# u = User('1abc@efg.com', 'hong')
# db_session.add(u)
# u = User('2abc@efg.com', 'hong2')
# db_session.add(u)
# u = User('3abc@efg.com', 'hong3')
# db_session.add(u)
# u = User('4abc@efg.com', 'hong4')
# db_session.add(u)
# u = User.query.filter(User.id == 2).first()
# print("user.id", u.id)
# u.email = 'pidokige.naver.com'
# db_session.add(u)
# db_session.commit()  # session made by flask
# ret = User.query.all()  # query all data.

# for r in ret:
#         print(r)  # display as tuple type
