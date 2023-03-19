from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, DateTime, TIMESTAMP, ForeignKey, PrimaryKeyConstraint, func, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# mysql_url = "mysql+pymysql://pidokige:Feb02pid~@localhost/flaskdb?charset=utf8"
mysql_url = "mysql+pymysql://pidokige:Feb02pid~@localhost/flaskdb?charset=utf8"

engine = create_engine(mysql_url, echo=True, pool_size=20, max_overflow=0)

print(engine)

db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

Base.metadata.create_all(bind=engine)

# class Movie(Base):
#     __tablename__ = 'movies'
#     id = Column(Integer, primary_key=True)
#     date = Column(Integer)
#     rank = Column(Integer)
#     movieNm = Column(String(30))
#     movieCd = Column(Integer)
#     salesAmt = Column(Integer)
#     audiCnt = Column(Integer)


# Movie.__table__.create(bind=engine, checkfirst=True)

db_session.remove()   # remove used db-session
