
from pydantic import BaseModel
class Student(BaseModel):
    id: int
    name: str
    section: str
    cgpa: float 