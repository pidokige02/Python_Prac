from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from init_db import Base, engine, db_session

class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    date = Column(Integer)
    rank = Column(Integer)
    movieNm = Column(String(30))
    movieCd = Column(Integer)
    salesAmt = Column(Integer)
    audiCnt = Column(Integer)


##################################################3
# ORM object declaration
class User(Base):
    __tablename__ = 'user_account'  # 데이터베이스에서 사용할 테이블 이름입니다.

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


print(User.__table__)
