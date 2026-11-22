from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    title: str
    summary: str
    link: str


class EmailDigest(BaseModel):
    ai: list[NewsItem] = Field(min_length=5, max_length=5)
    market: list[NewsItem] = Field(min_length=5, max_length=5)
