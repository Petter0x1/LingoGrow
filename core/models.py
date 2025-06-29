from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from os import makedirs
# Ensure the database folder exists
makedirs('database', exist_ok=True)


Base = declarative_base()

class Vocab(Base):
    __tablename__ = 'vocab'

    id = Column(Integer, primary_key=True)
    english = Column(String, nullable=False)
    arabic = Column(String, nullable=False)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    last_seen = Column(DateTime, default=datetime.utcnow)
    date_added = Column(DateTime, default=datetime.utcnow)
    difficulty = Column(String, default='medium')

class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)

engine = create_engine('sqlite:///database\\lingogrow.db')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def get_setting(session, key, default=None):
    setting = session.query(Settings).filter_by(key=key).first()
    return setting.value if setting else default

def set_setting(session, key, value):
    setting = session.query(Settings).filter_by(key=key).first()
    if setting:
        setting.value = str(value)
    else:
        setting = Settings(key=key, value=str(value))
        session.add(setting)
    session.commit()