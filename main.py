from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from database import get_db
from models import Player
from schemas import ScoreUpdate, PlayerScore, PlayerCreate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database import engine, Base
Base.metadata.create_all(bind=engine)

@app.post("/players/", response_model=List[PlayerScore])
def create_players(players: PlayerCreate, db: Session = Depends(get_db)):
    player_names = [players.player_one, players.player_two]
    created_players = []

    for name in player_names:
        db_player = db.query(Player).filter(Player.name == name).first()
        if db_player:
            raise HTTPException(status_code=400, detail=f"Player {name} already registered")
        
        new_player = Player(name=name, score=0)
        db.add(new_player)
        db.commit()
        db.refresh(new_player)
        created_players.append(new_player)
    
    return created_players

@app.post("/update_score/", response_model=PlayerScore)
def update_score(score_update: ScoreUpdate, db: Session = Depends(get_db)):
    print(f"Received update request: {score_update}")
    player = db.query(Player).filter(Player.name == score_update.name).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    if score_update.status == "WIN":
        player.score += 1
    elif score_update.status == "LOSE":
        player.score -= 1
    else:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    db.commit()
    db.refresh(player)
    return player

@app.get("/scores/", response_model=List[PlayerScore])
def read_scores(db: Session = Depends(get_db)):
    players = db.query(Player).order_by(Player.score.desc()).all()
    return players

@app.get("/player_score/{player_name}", response_model=PlayerScore)
def read_player_score(player_name: str, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.name == player_name).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
