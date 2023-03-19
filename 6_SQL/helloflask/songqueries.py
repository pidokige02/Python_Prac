from sqlalchemy import select
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import registry


from song_db import Base, engine, db_session
from songmodels import Album, Song, Artist, SongArtist, SongRank, User

################################################################3
# Album, Song table creation and data addtion to table (Done)
Album.__table__.create(bind=engine, checkfirst=True)
Song.__table__.create(bind=engine, checkfirst=True)
Artist.__table__.create(bind=engine, checkfirst=True)
SongArtist.__table__.create(bind=engine, checkfirst=True)
SongRank.__table__.create(bind=engine, checkfirst=True)
User.__table__.create(bind=engine, checkfirst=True)

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


################################################################3
# data addtion to SongRank table (Done)
# songrank_list = SongRank(id=1, rankdt='2022-9-28',songno='0000001',rank=1)
# db_session.add(songrank_list)

# songrank_list = SongRank(id=2, rankdt='2022-9-20',songno='0000002',rank=2)
# db_session.add(songrank_list)

# songrank_list = SongRank(id=3, rankdt='2022-10-28',songno='0000003',rank=3)
# db_session.add(songrank_list)

# db_session.commit()


#################################################################3
# # data addtion to SongRank table (not working)
# from sqlalchemy.orm import subqueryload, joinedload

# ret = Song.query.options(joinedload(Song.album)).filter(Song.likecnt < 10000).options(joinedload(Song.songartists)).options(
#         subqueryload(Song.songartists, SongArtist.artist)).order_by('atype')

# print(ret)

#################################################################3
# User data creation
u = User('1abc@efg.com', 'hong')
db_session.add(u)
u = User('2abc@efg.com', 'hong2')
db_session.add(u)
u = User('3abc@efg.com', 'hong3')
db_session.add(u)
u = User('4abc@efg.com', 'hong4')
db_session.add(u)
# u = User.query.filter(User.id == 2).first()
# print("user.id", u.id)
# u.email = 'pidokige.naver.com'
# db_session.add(u)
db_session.commit()  # session made by flask
ret = User.query.all()  # query all data.

for r in ret:
        print(r)  # display as tuple type
