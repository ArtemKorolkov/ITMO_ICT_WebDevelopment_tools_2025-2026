from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

# Перечисление рас (как в задании)
class RaceType(str, Enum):
    director = "director"
    worker = "worker"
    junior = "junior"

# Модель профессии
class Profession(BaseModel):
    id: int
    title: str
    description: str

# Модель умения
class Skill(BaseModel):
    id: int
    name: str
    description: str = ""  # пустая строка по умолчанию

# Модель воина (использует Profession и список Skill)
class Warrior(BaseModel):
    id: int
    race: RaceType
    name: str
    level: int
    profession: Profession
    skills: Optional[List[Skill]] = []  # по умолчанию пустой список