import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BasicTable(Base):
    """
    declarative
    """

    __tablename__ = 'BasicTable'

    id = Column(Integer, primary_key=True)
    basic = Column(String(128), unique=True)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)


class ComplexTable(Base):
    """
    declarative
    """

    __tablename__ = 'ComplexTable'

    id = Column(Integer, primary_key=True)
    itemId = Column(String(36))
    date = Column(DateTime)
    field1 = Column(Integer, default=0)
    field2 = Column(Integer, default=0)
    field3 = Column(Integer, default=0)
    field4 = Column(Integer, default=0)
    field5 = Column(Integer, default=0)
    field6 = Column(Integer, default=0)
    field7 = Column(Integer, default=0)
    field8 = Column(Integer, default=0)
    field9 = Column(Integer, default=0)
    field10 = Column(Integer, default=0)
    field11 = Column(Integer, default=0)
    field12 = Column(Integer, default=0)
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (UniqueConstraint('itemId', 'date', name='item_id_date'),
                      )


def db_init(db_engine):
    db_session = sessionmaker(bind=db_engine)
    session = db_session()
    Base.metadata.create_all(db_engine)
    return session
