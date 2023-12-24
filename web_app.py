import datetime
from typing import Dict, List
import fastapi
from fastapi import Depends, HTTPException
import json

from model import SozdanieZametki, InformZametk, TextZametki, SpisokZametok

api_router = fastapi.APIRouter()


def get_tokens() -> List[str]:
    try:
        with open("tokens.json", 'r', encoding='utf-8') as file:
            return json.load(file)
    # Обработка, если файл пустой
    except json.decoder.JSONDecodeError:
        return []


def verification_token(token: str, tokens: List[str] = Depends(get_tokens)):
    if token not in tokens:
        raise HTTPException(status_code=401, detail="Invalid token")


def zapis_id(id: int):
    with open("id.txt", "w") as file:
        file.write(str(id))


def zapis_zametki(text: str):
    with open("zametki.json", "w") as file:
        json.dump(text, file)


def polu4_zam() -> Dict[str, dict]:
    try:
        with open("zametki.json", "r", encoding='utf-8') as file:
            return json.load(file)
    # Обработка, если файл пустой
    except json.decoder.JSONDecodeError:
        return {}


def polu4_id():
    with open("id.txt", 'r') as file:
        current_id = int(file.read())
    return current_id


def save_note(notes: Dict[str, dict]):
    with open("zametki.json", 'w') as file:
        json.dump(notes, file)


#создание заметки
@api_router.post("/sozdanie_zametki", response_model=SozdanieZametki)
def s_z(text: str, token: str = Depends(verification_token)):
    id_staroe = polu4_id()
    id_new = str(id_staroe)
    notes = polu4_zam()
    now = datetime.datetime.now().isoformat()
    notes[id_new] = {
        "text": text,
        "created_at": now,
        "updated_at": now,
    }
    id_staroe += 1
    zapis_id(id_staroe)
    zapis_zametki(notes)
    return SozdanieZametki(
        id=id_new
    )


#чтение заметки
@api_router.get("/",response_model=TextZametki)
def read_note(id: str, token: str = Depends(verification_token)):
    note = polu4_zam()
    current_note = note[id]
    return TextZametki(
        id=id,
        text=current_note["text"]
    )


#получение информации о времени заметки
@api_router.post("/sozdanie_zametki/{id}/lolo", response_model=InformZametk)
def p_z(id: str, token: str = Depends(verification_token)):
    note = polu4_zam()
    note_id = note[id]
    return InformZametk(
        created_at=note_id["created_at"],
        updated_at=note_id["updated_at"]
    )

#изменить текст заметки
@api_router.post("/", response_model=TextZametki)
def change_the_text(id: str, text: str, token: str = Depends(verification_token)):
    note = polu4_zam()
    current_note = note[id]
    current_note["text"] = text
    zapis_zametki(note)
    return TextZametki(
        id=id,
        text=current_note["text"]
    )

#удалить заметку
@api_router.delete("/sozdanie_zametki/{id}/delete",response_model=TextZametki)
def delete_note(id: str, token: str = Depends(verification_token)):
    note = polu4_zam()
    current_note = note[id]
    note.pop(id)
    save_note(note)
    return TextZametki(
        id=id,
        text=current_note["text"]
    )

#вывести список заметок
@api_router.get("/list", response_model=SpisokZametok)
def list_notes(token: str = Depends(verification_token)):
    note = polu4_zam()
    keys_list = list(note.keys())
    dict_ids = {}
    for i in range(len(keys_list)):
        dict_ids[i] = keys_list[i]
    return SpisokZametok(
        counters=dict_ids
    )

