from fastapi import FastAPI
from typing import List, Dict, Any
from typing_extensions import TypedDict
from models import Warrior, Profession, RaceType

app = FastAPI()

# === Временная БД воинов ===
temp_bd: List[Dict[str, Any]] = [
    {
        "id": 1,
        "race": "director",
        "name": "Мартынов Дмитрий",
        "level": 12,
        "profession": {
            "id": 1,
            "title": "Влиятельный человек",
            "description": "Эксперт по всем вопросам"
        },
        "skills": [
            {"id": 1, "name": "Купле-продажа компрессоров", "description": ""},
            {"id": 2, "name": "Оценка имущества", "description": ""}
        ]
    },
    {
        "id": 2,
        "race": "worker",
        "name": "Андрей Косякин",
        "level": 12,
        "profession": {
            "id": 1,
            "title": "Дельфист-гребец",
            "description": "Уважаемый сотрудник"
        },
        "skills": []
    }
]

# === Временная БД профессий ===
professions_bd: List[Dict[str, Any]] = [
    {"id": 1, "title": "Влиятельный человек", "description": "Эксперт по всем вопросам"},
    {"id": 2, "title": "Дельфист-гребец", "description": "Уважаемый сотрудник"}
]

# === Корневой эндпоинт ===
@app.get("/")
def root():
    return {"message": "Hello, [Ваше Имя]!"}

# === Эндпоинты для воинов ===
@app.get("/warriors_list", response_model=List[Warrior])
def warriors_list() -> List[Warrior]:
    return temp_bd

@app.get("/warrior/{warrior_id}", response_model=List[Warrior])
def warriors_get(warrior_id: int) -> List[Warrior]:
    return [w for w in temp_bd if w.get("id") == warrior_id]

class WarriorResponse(TypedDict):
    status: int
    data: Warrior

@app.post("/warrior", response_model=WarriorResponse)
def warriors_create(warrior: Warrior) -> WarriorResponse:
    temp_bd.append(warrior.model_dump())
    return {"status": 200, "data": warrior}

@app.delete("/warrior/delete{warrior_id}")
def warrior_delete(warrior_id: int):
    for i, w in enumerate(temp_bd):
        if w.get("id") == warrior_id:
            temp_bd.pop(i)
            return {"status": 201, "message": "deleted"}
    return {"status": 404, "message": "not found"}

@app.put("/warrior{warrior_id}", response_model=List[Warrior])
def warrior_update(warrior_id: int, warrior: Warrior) -> List[Warrior]:
    for i, w in enumerate(temp_bd):
        if w.get("id") == warrior_id:
            temp_bd[i] = warrior.model_dump()
            break
    return temp_bd

# === Эндпоинты для профессий ===
@app.get("/professions", response_model=List[Profession])
def get_professions() -> List[Profession]:
    return professions_bd

@app.get("/profession/{prof_id}", response_model=Profession)
def get_profession(prof_id: int):
    for p in professions_bd:
        if p["id"] == prof_id:
            return p
    return {"error": "Profession not found"}

@app.post("/profession", response_model=Profession)
def create_profession(profession: Profession):
    for p in professions_bd:
        if p["id"] == profession.id:
            return {"error": "ID already exists"}
    professions_bd.append(profession.model_dump())
    return profession

@app.put("/profession/{prof_id}", response_model=Profession)
def update_profession(prof_id: int, profession: Profession):
    for i, p in enumerate(professions_bd):
        if p["id"] == prof_id:
            professions_bd[i] = profession.model_dump()
            return profession
    return {"error": "Profession not found"}

@app.delete("/profession/{prof_id}")
def delete_profession(prof_id: int):
    for i, p in enumerate(professions_bd):
        if p["id"] == prof_id:
            professions_bd.pop(i)
            return {"status": "deleted"}
    return {"error": "Profession not found"}