from pydantic import BaseModel

class PlayerCreate(BaseModel):
    player_one: str
    player_two: str

class ScoreUpdate(BaseModel):
    name: str
    status: str

class PlayerScore(BaseModel):
    name: str
    score: int

    class Config:
        orm_mode = True
