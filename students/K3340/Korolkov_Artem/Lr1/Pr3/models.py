from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# ---------- Перечисление рас ----------
class RaceType(str, Enum):
    director = "director"
    worker = "worker"
    junior = "junior"

# ---------- Ассоциативная таблица для Many-to-Many (воин-скилл) ----------
class SkillWarriorLink(SQLModel, table=True):
    skill_id: int = Field(default=None, foreign_key="skill.id", primary_key=True)
    warrior_id: int = Field(default=None, foreign_key="warrior.id", primary_key=True)
    level: Optional[int] = None   # новое поле (Изменение модели – добавляем поле level в ассоциативную таблицу

# ---------- Модель Skill (умение) ----------
class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = ""
    # Обратная связь: список воинов, владеющих этим умением
    warriors: Optional[List["Warrior"]] = Relationship(
        back_populates="skills",
        link_model=SkillWarriorLink
    )

# ---------- Модель Profession (профессия) ----------
class Profession(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    # Один-ко-многим: у профессии может быть много воинов
    warriors_prof: List["Warrior"] = Relationship(back_populates="profession")

# ---------- Базовая модель воина (без id и связей) для POST/PATCH ----------
class WarriorDefault(SQLModel):
    race: RaceType
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")

# ---------- Полная модель воина (таблица в БД) ----------
class Warrior(WarriorDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    # Связь с профессией (многие-к-одному)
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof")
    # Связь с умениями (многие-ко-многим)
    skills: Optional[List[Skill]] = Relationship(
        back_populates="warriors",
        link_model=SkillWarriorLink
    )

# ---------- Модель для ответа с вложенной профессией ----------
class WarriorWithProfession(WarriorDefault):
    profession: Optional[Profession] = None

# ---------- Модель для ответа с вложенными умениями ----------
class WarriorWithSkills(WarriorDefault):
    skills: Optional[List[Skill]] = []



class ProfessionDefault(SQLModel):
    title: str
    description: str

'''class Profession(ProfessionDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    warriors_prof: List["Warrior"] = Relationship(back_populates="profession")'''



class SkillDefault(SQLModel):
    name: str
    description: Optional[str] = ""

'''class Skill(SkillDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    warriors: Optional[List["Warrior"]] = Relationship(back_populates="skills", link_model=SkillWarriorLink)'''