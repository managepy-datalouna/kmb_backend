from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.staticfiles import StaticFiles

from typing import List, Optional
from pydantic import BaseModel

DATABASE_URL = "sqlite:///../base.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PlayerModel(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    matches = Column(Integer)

Base.metadata.create_all(bind=engine)

# Pydantic схема для создания и обновления игрока
class PlayerCreate(BaseModel):
    name: str
    matches: int

# Pydantic схема для отображения игрока
class Player(BaseModel):
    id: int
    name: str
    matches: int

    class Config:
        orm_mode = True

app = FastAPI()

app.mount("/static", StaticFiles(directory="../kmb_frontend"), name="static")

# Получение сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/players/", response_model=Player)
def create_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_player = PlayerModel(name=player.name, matches=player.matches)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

@app.get("/players/", response_model=List[Player])
def read_players(db: Session = Depends(get_db)):
    players = db.query(PlayerModel).all()
    return players

@app.get("/players/{player_id}", response_model=Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(PlayerModel).filter(PlayerModel.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

# @app.put("/players/{player_id}", response_model=Player)
# def update_player(player_id: int, player: PlayerCreate, db: Session = Depends(get_db)):
    # db_player = db.query(PlayerModel).filter(PlayerModel.id == player_id).first()
    # if db_player is None:
        # raise HTTPException(status_code=404, detail="Player not found")
    # db_player.name = player.name
    # db_player.matches = player.matches
    # db.commit()
    # db.refresh(db_player)
    # return db_player

@app.delete("/players/{player_id}", response_model=Player)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(PlayerModel).filter(PlayerModel.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    db.delete(player)
    db.commit()
    return player
