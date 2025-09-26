from pydantic import BaseModel, field_validator
from typing import Optional
import bleach

ALLOWED_TAGS = ["p", "br", "strong", "em", "ul", "ol", "li", "a", "h1", "h2", "h3", "h4", "blockquote", "code", "pre"]
ALLOWED_ATTRIBUTES = {"a": ["href", "title"], "img": ["alt"]}

# User Schema
class PostBase(BaseModel):
    pass

class PostCreate(PostBase):
    title: str
    content: str
    category_id: Optional[int] = None

    @field_validator("content")
    def sanitize_content(cls, value:str):
        cleaned = bleach.clean(value, tags = ALLOWED_TAGS, attributes= ALLOWED_ATTRIBUTES, strip=True)
        return cleaned

class PostUpdate(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None

    @field_validator("content")
    def sanitize_content(cls, value:str):
        cleaned = bleach.clean(value, tags = ALLOWED_TAGS, attributes= ALLOWED_ATTRIBUTES, strip=True)
        return cleaned