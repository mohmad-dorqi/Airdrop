from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    coins = Column(Integer, default=0)
    has_clicker_bot = Column(Boolean, default=False)
    multitap_level = Column(Integer, default=1)
    recharge_level = Column(Integer, default=1)
    referral_link = Column(String, unique=True)
    referred_count = Column(Integer, default=0)
    wallet_address = Column(String, nullable=True)
    game_2048_score = Column(Integer, default=0)
    total_contributed_to_referrer = Column(Integer, default=0)
    
    referred_users = relationship("ReferredUser", back_populates="referrer")

class ReferredUser(Base):
    __tablename__ = 'referred_users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    coins = Column(Integer, default=0)
    referrer_id = Column(Integer, ForeignKey('users.id'))

    referrer = relationship("User", back_populates="referred_users")

class Advertisement(Base):
    __tablename__ = 'advertisements'
    
    id = Column(Integer, primary_key=True)
    link = Column(String, nullable=False)
    text = Column(String, nullable=False)

def init_db():
    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

Session = init_db()
