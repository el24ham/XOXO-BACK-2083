from sqlalchemy import Column, Integer, String, Sequence
from database import Base

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, Sequence('player_id_seq'), primary_key=True)
    name = Column(String(50), unique=True, index=True)
    score = Column(Integer, default=0)
