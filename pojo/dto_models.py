from pydantic import BaseModel


class ImageRequestDto(BaseModel):
    imageByte: str
    username: str
