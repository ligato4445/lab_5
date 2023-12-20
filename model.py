from typing import Dict

from pydantic import BaseModel


class SozdanieZametki(BaseModel):
    id: int

class InformZametk(BaseModel):
    created_at: str
    updated_at: str

class TextZametki(BaseModel):
    id: int
    text: str

class SpisokZametok(BaseModel):
    counters: Dict[int, str]

