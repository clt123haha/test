from sqlalchemy import Column, String, Integer,DATETIME,FLOAT,BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:yueye13084030!@gz-cynosdbmysql-grp-ro694ctz.sql.tencentcdb.com:28492/exchange", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True)
    phone = Column(String(20))
    email = Column(String(50))
    password = Column(String(50))
    birthday =  Column(String(10))
    sid = Column(Integer)

    def __repr__(self):
        ID = self.id
        PHONE = self.phone
        PASSWORD = self.password
        EMAIL = self.email
        SID = self.sid
        return f"User: phone: {PHONE},page:{PASSWORD},email:{EMAIL},id: {ID},sid:{SID}"



class ShortMessage(Base):
    __tablename__ = "shortMessage"
    id = Column(Integer, primary_key=True)
    phonenumber = Column(String(20))
    meaasge = Column(String(10))
    time = Column(String(30))

    def __repr__(self):
        ID = self.id
        PHONENUMBER = self.phonenumber
        MESSAGE = self.meaasge
        TIME = self.time
        return f"User: phonenumber: {PHONENUMBER},message:{MESSAGE},time:{TIME},id: {ID}"

class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    seller = Column(Integer)
    price = Column(Integer)
    system= Column(String(20))
    addiction= Column(BOOLEAN)
    channel  = Column(String(30))
    login_method = Column(String(30))
    approved = Column(BOOLEAN)

    def __repr__(self):
        ID = self.id
        PRICE = self.price
        ADDICTION = self.addiction
        CHANNEL = self.channel
        LOGIN_METHOD = self.login_method
        SELLER = self.seller
        APPROVED = self.approved
        SYSTEM = self.system


        return f"User: price: {PRICE},addiction:{ADDICTION},channel:{CHANNEL},id: {ID},login_method:{LOGIN_METHOD},seller:{SELLER},approved:{APPROVED},system:{SYSTEM}"


class User_History(Base):  # 历史记录
    __tablename__ = 'user_history'
    id = Column(Integer, primary_key=True)
    history = Column(Integer, primary_key=True)  # 外键
    fav = Column(Integer, nullable=False, default=0)  # default默认值

    def __repr__(self):
        ID = self.id
        History = self.history
        FAV = self.fav
        return f"User:id:{ID},history:{History},fav:{FAV}"

class History(Base):  # 历史记录的具体内容
    __tablename__ = 'history'
    gamename = Column(String(255), nullable=False)
    rid = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        ID = self.id
        RID = self.rid
        GAMENAME = self.gamename
        return f"User:id:{ID},rid:{RID},gamename:{GAMENAME}"

class Audit(Base):  # 历史记录的具体内容
    __tablename__ = 'audit'
    type = Column(String(20), nullable=False)
    ifpass = Column(BOOLEAN, nullable=False)
    uid = Column(Integer)
    message = Column(String(20), nullable=False)
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        ID = self.aid
        UID = self.uid
        TYPE = self.type
        IFPASS = self.ifpass
        MESSAGE = self.message
        return f"User:id:{ID},uid:{UID},ifpass:{IFPASS},type:{TYPE},message:{MESSAGE}"

class Blacklist(Base):  # 历史记录的具体内容
    __tablename__ = 'blacklist'

    uid = Column(Integer)
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        ID = self.aid
        UID = self.uid

        return f"User:id:{ID},uid:{UID}"

class Admin(Base):  # 历史记录的具体内容
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    account = Column(String(20),nullable=False)
    password = Column(String(20), nullable=False)

    def __repr__(self):
        ID = self.aid
        ACCOUNT = self.account
        PASSWORD = self.password
        return f"User:id:{ID},account:{ACCOUNT},password:{PASSWORD}"

def get_sheet():
    {
    Base.metadata.create_all(engine)  # 通过此语句创建表
}