import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship

engine = create_engine("mysql+pymysql://root:123456@10.178.233.181/dmsedt")
# engine = create_engine("mysql://root:123456@10.178.233.181/dmsedt?charset=utf8",pool_size=8)

Base = declarative_base()



class Mf4PathInfo(Base):

    __tablename__ = "mf4path"

    mf4pathid = Column(Integer, primary_key=True, autoincrement=True)
    mf4path = Column(String(255))
    mf4filenumber = Column(Integer)

    def __init__(self, mf4path, mf4filenumber):
        self.mf4path = mf4path
        self.mf4filenumber = mf4filenumber



class Mf4FileInfo(Base):
    __tablename__ = "mf4file"

    mf4fileid = Column(Integer, primary_key=True, autoincrement=True)
    mf4name = Column(String(50))
    imgoutputpath = Column(String(255))
    imgnumber = Column(Integer, default=6)
    isok = Column(Boolean, default=0)
    mf4pathid = Column(Integer,ForeignKey(Mf4PathInfo.mf4pathid))

    mf4path = relationship(Mf4PathInfo,uselist=True)

    def __init__(self, mf4name, imgoutputpath, mf4pathid):
        self.mf4name = mf4name
        self.imgoutputpath = imgoutputpath
        self.mf4pathid = mf4pathid
        


def create_table():
    ...
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":

    create_table()


