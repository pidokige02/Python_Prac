from sqlalchemy import select
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import registry


from init_db import Base, engine, db_session
from models import Movie, User, Address


################################################################
# 데이터베이스 메타데이터로 작업하기 (다른 file 의 class 를 이용하지 않고 여기서 직접정의하여 table 을 만든다)
# metadata = MetaData()  # 테이블들의 메타 정보를 담게될 객체입니다.

# user_table = Table(
#         'user_account',  # 데이터베이스에 저장될 table 이름입니다.
#         metadata,
#         Column('id', Integer, primary_key=True),  # 이 테이블에 들어갈 컬럼입니다.
#         Column('name', String(30)),
#         Column('fullname', String),
#     )

# print(user_table.c.name)

# print(user_table.c.keys())      # acquiring key value

# print(user_table.primary_key)   # getting primary key information for table

# address_table = Table(
#      "address",
#      metadata,
#      Column('id', Integer, primary_key=True),
#      Column('user_id', ForeignKey('user_account.id'), nullable=False),  # ForeignKey 객체로 외래 키를 선언합니다.
#      Column('email_address', String, nullable=False)
# )

# #위에서 선언한 table 'address' and 'user_account' 을 하래 command 를 이용히여 database 에 실제로 생성된다.
# metadata.create_all(engine)
################################################################3

################################################################3
# # ORM 방식으로 테이블 메타데이터 정의하기
# mapper_registry = registry()
# mapper_registry.metadata

# # ORM 객체 생성하기
# sandy = User(name="sandy", fullname="Sandy Cheeks")
# print("jinha",sandy)

# # ORM으로 선언한 테이블을 실제로 데이터베이스에 적용
# mapper_registry.metadata.create_all(engine)
# Base.metadata.create_all(engine)

# # DATA ADDITION TO TABLE
# movie_list=Movie(date=20190625, rank=1, movieNm='토이 스토리4', movieCd=12345, salesAmt=1234545123,audiCnt=342)

# db_session.add(movie_list)
# db_session.commit()


################################################################3
# table creation and data addtion to table
# Movie.__table__.create(bind=engine, checkfirst=True)

# movie_list=Movie(date=20190625, rank=1, movieNm='토이 스토리4', movieCd=12345, salesAmt=1234545123,audiCnt=342)

# db_session.add(movie_list)
# db_session.commit()


################################################################3
# query all movies data
# result = db_session.query(Movie).all()
# for row in result:
#   print(row.date,row.rank,row.movieNm,row.movieCd,row.salesAmt,row.audiCnt)


################################################################3
# query all movies data w/ condition
# stmt = select(Movie).where(Movie.audiCnt == '342')
# print(stmt)

# with engine.connect() as conn:
#     for row in conn.execute(stmt):
#        print(row)


################################################################3
# insert() 를 통한 SQL 표현식 구성 and 명령문 실행
# from sqlalchemy import insert
# stmt = insert(User).values(name='spongebob', fullname="Spongebob Squarepants")
# print(stmt)
# compiled = stmt.compile()
# print(compiled.params)

# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     print(result.inserted_primary_key)
#     conn.commit()


################################################################3
# Connection.execute() 에 INSERT 매개변수 전달하기
# from sqlalchemy import insert

# with engine.connect() as conn:
#      result = conn.execute(
#          insert(User),
#          [
#              {"name": "sandy", "fullname": "Sandy Cheeks"},
#              {"name": "patrick", "fullname": "Patrick Star"}
#          ]
#      )
#      conn.commit()


################################################################3
# update() 를 통한 SQL 표현식 구성 and commit
# from sqlalchemy import update

# stmt = (
#      update(User).where(User.name == 'patrick').
#      values(fullname='Patrick the Star')
# )

# print(stmt)

# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     conn.commit()

################################################################
# SELECT 하여 받은 행들을 INSERT 하기 위한 쿼리 (Done)
# from sqlalchemy import insert

# select_stmt = select(User.id, User.name + "@aol.com")
# insert_stmt = insert(Address).from_select(
#     ["user_id", "email_address"], select_stmt)
# print(insert_stmt)

# with engine.connect() as conn:
#     result = conn.execute(insert_stmt)
#     conn.commit()


################################################################
# Correlated 업데이트
# from sqlalchemy import update

# scalar_subq = (
#    select(Address.email_address).
#    where(Address.user_id == User.id).
#    order_by(Address.id).
#    limit(1).
#    scalar_subquery()
# )

# update_stmt = update(User).values(fullname=scalar_subq)
# print(update_stmt)

# with engine.connect() as conn:
#     result = conn.execute(update_stmt)
#     conn.commit()

################################################################
# 다른 테이블과 연관된 조건으로 업데이트 (not working)
# from sqlalchemy import update

# update_stmt = (
#     update(User).
#     where(User.id == Address.user_id).
#     where(Address.email_address == 'patrick@aol.com').
#     values(fullname='Pat')
#   )

# print(update_stmt)

# with engine.connect() as conn:
#     result = conn.execute(update_stmt)
#     conn.commit()

################################################################
# delete() 를 통한 SQL 표현식 구성 (Done)

# from sqlalchemy import delete
# stmt = delete(User).where(User.name == 'patrick')
# print(stmt)

# with engine.connect() as conn:
#     result = conn.execute(stmt)
#     conn.commit()


################################################################
# UPDATE, DELETE에서 영향을 받는 행 수 얻기 (Done)
# from sqlalchemy import update

# with engine.begin() as conn:
#      result = conn.execute(
#         update(User).
#         values(fullname="Patrick McStar").
#         where(User.name == 'patrick')
#     )
# print(result.rowcount)  # Result 객체의 rowcount 속성을 사용합니다.


################################################################
# UPDATE, DELETE와 함께 RETURNING 사용하기 (not working)
# from sqlalchemy import update

# update_stmt = (
#     update(User).where(User.name == 'patrick').
#     values(fullname='Patrick the Star').
#     returning(User.id, User.name)
# )

# print(update_stmt)

# with engine.connect() as conn:
#     result = conn.execute(update_stmt)
#     conn.commit()


################################################################
# 관계된 객체 사용하기
# u1 = User(name='pkrabs', fullname='Pearl Krabs')
# print(u1.addresses)
# a1 = Address(email_address="pear1.krabs@gmail.com")
# u1.addresses.append(a1)
# print(u1.addresses)
# print(a1.user)  # relationship.back_populates 을 사용한 동기화됨

# a2 = Address(email_address="pearl@aol.com", user=u1)  #a2.user = u1
# print(u1.addresses)  #pear1.krabs@gmail.com 와 pearl@aol.com 이 표시됨
# db_session.add(u1)
# db_session.commit()

################################################################
# relationship()을 사용하여 조인하기
# print(
#     select(Address.email_address).
#     select_from(User).
#     join(User.addresses)
# )

# select_smt = (
#     select(Address.email_address).
#     select_from(User).
#     join(User.addresses)
# )

# ret = db_session.execute(select_smt).all()
# print(ret)

# print(
#     select(Address.email_address).
#     join_from(User, Address)
# )

# select_smt = (
#     select(Address.email_address).
#     join_from(User, Address)
# )

# ret = db_session.execute(select_smt).all()
# print(ret)

################################################################
# 별칭(aliased)을 사용하여 조인하기
# from sqlalchemy.orm import aliased
# address_alias_1 = aliased(Address)
# address_alias_2 = aliased(Address)

# print(
#     select(User).
#     join_from(User, address_alias_1).
#     where(address_alias_1.email_address == 'patrick@aol.com').
#     join_from(User, address_alias_2).
#     where(address_alias_2.email_address == 'patrick@gmail.com')
# )

# select_smt = (
#     select(User).
#     join_from(User, address_alias_1).
#     where(address_alias_1.email_address == 'patrick@aol.com').
#     join_from(User, address_alias_2).
#     where(address_alias_2.email_address == 'patrick@gmail.com')
# )

# ret = db_session.execute(select_smt).all()
# print(ret)

################################################################
# ON 조건 확대
stmt = (
    select(User.fullname).
    join(User.addresses.and_(Address.email_address == 'pearl.krabs@gmail.com'))
)

print(stmt)

ret = db_session.execute(stmt).all()
print(ret)

################################################################
# EXISTS has() , and()
stmt = (
    select(User.fullname).
    where(User.addresses.any(Address.email_address == 'pearl.krabs@gmail.com'))
)

ret = db_session.execute(stmt).all()
print(ret)
