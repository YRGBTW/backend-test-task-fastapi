from pydantic import BaseModel

# User Schema
class CategoryBase(BaseModel):
    pass

class CategoryCreate(CategoryBase):
    title: str